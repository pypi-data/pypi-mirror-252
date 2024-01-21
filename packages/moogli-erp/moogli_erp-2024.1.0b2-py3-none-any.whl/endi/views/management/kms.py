import logging
import datetime

from sqlalchemy import distinct
from endi_base.models.base import DBSESSION
from endi.export.utils import write_file_to_request
from endi.export.excel import XlsExporter
from endi.export.ods import OdsExporter
from endi.models.user import User
from endi.models.expense.sheet import ExpenseSheet, ExpenseKmLine
from endi.views import BaseView


logger = logging.getLogger(__name__)


class KmsManagementTools:
    """
    Fonctions utilitaires pour le suivi des kilomètres
    """

    def users_with_kms(self, years=[]):
        """
        Retourne les ids des utilisateurs ayant validé des kms
        sur les années passées en paramètre
        """
        sheets = (
            DBSESSION()
            .query(distinct(ExpenseSheet.user_id))
            .filter(ExpenseSheet.year.in_(years))
            .filter(ExpenseSheet.status == "valid")
            .filter(ExpenseSheet.kmlines.any())
        )
        return [sheet[0] for sheet in sheets.all()]

    def get_user_year_kms(self, user_id, year):
        """
        Retourne le nombre de kms validés pour un utilisateur sur l'année donnée
        """
        sheets = (
            ExpenseSheet.query()
            .filter(ExpenseSheet.year == year)
            .filter(ExpenseSheet.user_id == user_id)
            .filter(ExpenseSheet.status == "valid")
            .filter(ExpenseSheet.kmlines.any())
        )
        sheets_id = [sheet.id for sheet in sheets.all()]
        kmlines = (
            ExpenseKmLine.query().filter(ExpenseKmLine.sheet_id.in_(sheets_id)).all()
        )
        return sum([line.km for line in kmlines])

    def compute_kms_datas(self, years):
        """
        Calcule les indicateurs de suivi pour chaque utilisateur
        sur les années passées en paramètre
        """
        kms_datas = []
        users = self.users_with_kms(years)
        for user_id in users:
            user = User.get(user_id)
            user_kms = {}
            for y in years:
                user_kms[y] = self.get_user_year_kms(user_id, y)
            kms_datas.append(
                {
                    "user_id": user_id,
                    "user_label": f"{user.lastname} {user.firstname}",
                    "user_kms": user_kms,
                }
            )
        return sorted(kms_datas, key=lambda item: item["user_label"])

    def compute_total_kms(self, years, kms_datas):
        """
        Calcule les totaux à partir des données des utilisateurs
        """
        total_kms = {}
        for y in years:
            total_kms[y] = 0
        for data in kms_datas:
            for y in years:
                total_kms[y] += data["user_kms"][y]
        return total_kms


class KmsManagementView(BaseView, KmsManagementTools):
    """
    Tableau de suivi des kilomètres pour les 3 dernières années
    """

    title = "Suivi des kilomètres par salarié"

    def __call__(self):
        years = [
            datetime.date.today().year,
            datetime.date.today().year - 1,
            datetime.date.today().year - 2,
        ]
        kms_datas = self.compute_kms_datas(years)
        total_kms = self.compute_total_kms(years, kms_datas)

        return dict(
            title=self.title,
            years=years,
            kms_datas=kms_datas,
            total_kms=total_kms,
            export_xls_url=self.request.route_path(
                "management_kms_export",
                extension="xls",
                _query=self.request.GET,
            ),
            export_ods_url=self.request.route_path(
                "management_kms_export",
                extension="ods",
                _query=self.request.GET,
            ),
        )


class KmsManagementXlsView(BaseView, KmsManagementTools):
    """
    Export du tableau de suivi des kms au format XLS
    """

    _factory = XlsExporter

    @property
    def filename(self):
        return "suivi_kms_{}.{}".format(
            datetime.date.today().strftime("%Y-%m-%d"),
            self.request.matchdict["extension"],
        )

    def __call__(self):
        writer = self._factory()
        writer._datas = []
        # Récupération des données
        years = [
            datetime.date.today().year,
            datetime.date.today().year - 1,
            datetime.date.today().year - 2,
        ]
        kms_datas = self.compute_kms_datas(years)
        total_kms = self.compute_total_kms(years, kms_datas)
        # En-têtes
        headers = [
            "Salarié",
        ]
        for y in years:
            headers.append(f"Nb Km {y}")
        writer.add_headers(headers)
        # Données des enseignes
        for data in kms_datas:
            row_data = [
                data["user_label"],
            ]
            for y in years:
                row_data.append(data["user_kms"][y] / 100)
            writer.add_row(row_data)
        # Total
        row_total = [
            "TOTAL",
        ]
        for y in years:
            row_total.append(total_kms[y] / 100)
        writer.add_row(row_total, options={"highlighted": True})
        # Génération du fichier d'export
        write_file_to_request(self.request, self.filename, writer.render())
        return self.request.response


class KmsManagementOdsView(KmsManagementXlsView):
    """
    Export du tableau de suivi des kms au format ODS
    """

    _factory = OdsExporter


def includeme(config):
    config.add_route("management_kms", "management/kms")
    config.add_route("management_kms_export", "management/kms.{extension}")
    config.add_view(
        KmsManagementView,
        route_name="management_kms",
        renderer="management/kms.mako",
        permission="view.expensesheet",
    )
    config.add_view(
        KmsManagementXlsView,
        route_name="management_kms_export",
        match_param="extension=xls",
        permission="view.expensesheet",
    )
    config.add_view(
        KmsManagementOdsView,
        route_name="management_kms_export",
        match_param="extension=ods",
        permission="view.expensesheet",
    )
    config.add_admin_menu(
        parent="management",
        order=0,
        label="Suivi des kilomètres",
        href="/management/kms",
    )
