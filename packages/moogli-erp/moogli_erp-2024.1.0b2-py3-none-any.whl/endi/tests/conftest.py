import datetime
import os
import sys

from pytest import fixture, mark
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from pyramid.request import apply_request_extensions
from pyramid.interfaces import IRoutesMapper
from pyramid_beaker import BeakerSessionFactoryConfig
from sqlalchemy import engine_from_config
import endi
from endi import models  # noqa : W0611
from endi.utils.filedepot import (
    configure_filedepot,
)
from endi.utils.widgets import (
    ActionMenu,
    Navigation,
)
from endi.tests.tools import DummyRouteContext, DummyRoute

HERE = os.path.dirname(__file__)
DATASDIR = os.path.join(HERE, "datas")
TMPDIR = os.path.join(HERE, "tmp")


def pytest_addoption(parser):
    parser.addoption(
        "--endi-plugins",
        nargs="*",
        default=[],
        help="endi plugin(s) to test : sap",
    )


def pytest_collection_modifyitems(config, items):
    plugins = config.getoption("--endi-plugins")
    active_plugin_marks = [f"plugin_{i}" for i in plugins]

    for item in items:
        skiped_plugins = [
            kw
            for kw in item.keywords
            if kw.startswith("plugin_") and kw not in active_plugin_marks
        ]
        if len(skiped_plugins) > 0:
            skip_plugin = mark.skip(reason="need --endi-plugins <plugin>")
            item.add_marker(skip_plugin)


def pytest_configure(config):
    endi._called_from_test = True


def __current_test_ini_file():
    local_test_ini = os.path.join(HERE, "../../test.ini")
    if os.path.exists(local_test_ini):
        return local_test_ini
    return os.path.join(HERE, "../../gitlab-ci.ini")


def launch_cmd(cmd):
    """
    Main entry to launch os commands
    """
    print(("Launching : %s" % cmd))
    return os.system(cmd)


def mysql_test_connect(settings):
    """
    test the db connection
    """
    cmd = settings["connect"]
    ret_code = launch_cmd(cmd)

    if ret_code != 0:
        err_str = (
            """
    actual err_code = %s\n

    1- You need to configure the test.ini file so that this script can connect\n
    to the Mysql database:

        ...\n
        testdb.sql_cmd=mysql --defaults-file=/etc/mysql/debian.cnf\n
        ...\n
    or\n
        ...\n
        testdb.sql_cmd=mysql -uroot -p<password>\n
        ...\n


    2- Ensure mysql server is started and reachable with the given configuration
        """
            % ret_code
        )

        print(err_str)
        sys.exit(err_str)


def create_sql_user(settings):
    """
    Create the sql test user
    """
    launch_cmd(settings["adduser"])


def create_test_db(settings):
    """
    Create the test database and grant rights
    """
    launch_cmd(settings["adddb"])


def get_test_options_from_settings(settings):
    prefix = "testdb."
    options = {}
    for key in settings:
        if key.startswith(prefix):
            options[key[len(prefix) :]] = settings[key]
    return options


def initialize_test_database(settings):
    """
    dump sample datas as a test database
    """
    if __current_test_ini_file().endswith("gitlab-ci.ini"):
        return
    options = get_test_options_from_settings(settings)
    os.putenv("SHELL", "/bin/bash")
    mysql_test_connect(options)
    create_sql_user(options)
    launch_cmd(options["drop"])
    create_test_db(options)


@fixture
def fixture_factory(dbsession):
    def _fixture_factory(ModelFactory, **defaults):
        """
        Factorize standard model factories (mk_*)

        It allow to provide defaults, and of course ad-hoc values that can take
        precedence over default values.

        Intented for simple models

        DO NOT work for relation attributes

        :param **default dict: the default attributes values.
        """

        def factory(**kwargs):
            props = {}
            props.update(defaults)
            props.update(kwargs)

            obj = ModelFactory(**props)
            dbsession.add(obj)
            dbsession.flush()
            return obj

        return factory

    return _fixture_factory


@fixture
def today():
    return datetime.date.today()


@fixture
def date_20190101():
    return datetime.date(2019, 1, 1)


@fixture
def date_20200101():
    return datetime.date(2020, 1, 1)


@fixture
def date_20210101():
    return datetime.date(2021, 1, 1)


@fixture(scope="session")
def filesystem(request):
    os.system("mkdir -p {}".format(TMPDIR))

    def remove_files():
        print("Removing files from the TMP directory {}".format(TMPDIR))
        if __current_test_ini_file().endswith("gitlab-ci.ini"):
            return
        os.system("rm -rf {}/*".format(TMPDIR))
        print("Done")

    request.addfinalizer(remove_files)
    return request


@fixture(scope="session")
def base_settings(filesystem):
    _settings = appconfig("config:%s" % __current_test_ini_file(), "endi")
    _settings["endi.ftpdir"] = DATASDIR
    return _settings


@fixture(scope="session")
def plugin_active(request):
    def _plugin_active(plugin_name):
        return plugin_name in request.config.getoption("endi_plugins")

    return _plugin_active


@fixture(scope="session")
def settings(base_settings, plugin_active):
    """
    base_settings/settings decoupling is to allow settings fixture
    inheritance/overriding without repetition.
    """

    if plugin_active("sap"):
        base_settings["endi.includes"] = "endi.plugins.sap"
    if plugin_active("sap_urssaf3p"):
        base_settings["endi.includes"] = "endi.plugins.sap\nendi.plugins.sap_urssaf3p"
    return base_settings


@fixture
def registry(settings):
    from pyramid.registry import Registry

    registry = Registry()
    registry.settings = settings
    yield registry
    del registry


@fixture
def pyramid_request(registry, settings):
    request = testing.DummyRequest()
    setattr(request, "referrer", "")
    setattr(request, "referer", "")
    request.registry = registry
    setup_pyramid_layout(request, context=None)
    return request


@fixture
def config(request, pyramid_request, settings, registry):
    """
    returns a Pyramid `Configurator` object initialized with default settings
    """
    print("Setting up config")
    os.environ["TZ"] = "Europe/Paris"
    from pyramid_beaker import set_cache_regions_from_settings

    config = testing.setUp(
        registry=registry, settings=settings, request=pyramid_request
    )
    for include in settings["pyramid.includes"].split("\n"):
        include = include.strip()
        if include:
            config.include(include)
    set_cache_regions_from_settings(settings)
    request.addfinalizer(testing.tearDown)
    configure_filedepot(settings)

    from endi import (
        config_services,
        add_static_views,
        include_custom_modules,
        add_base_directives_and_predicates,
    )

    from endi.utils.renderer import customize_renderers

    config.include(config_services)
    customize_renderers(config)
    add_base_directives_and_predicates(config)
    add_static_views(config, settings)
    config.include("endi_celery")

    config.include("endi.utils.modules")
    include_custom_modules(config)

    config.include("endi.utils.notification")

    config.include("endi.subscribers.before_render")
    print("Configuring panels")
    from endi import ENDI_PANELS_MODULES

    for module in ENDI_PANELS_MODULES:
        config.include(module)

    apply_request_extensions(pyramid_request)
    yield config
    testing.tearDown()


@fixture
def request_with_config(config, pyramid_request):
    return pyramid_request


@fixture(scope="session")
def connection(request, settings):
    """sets up a SQLAlchemy engine and returns a connection
    to the database.

    :param settings: the settings of the test (given by the testing
    fixture)
    :returns: a sqlalchemy connection object
    """
    # the following setup is based on `kotti.resources.initialize_sql`,
    # except that it explicitly binds the session to a specific connection
    # enabling us to use savepoints independent from the orm, thus allowing
    # to `rollback` after using `transaction.commit`...
    initialize_test_database(settings)

    from endi_base.models.base import DBSESSION, DBBASE

    engine = engine_from_config(settings, prefix="sqlalchemy.")
    _connection = engine.connect()
    DBSESSION.registry.clear()
    DBSESSION.configure(bind=engine)
    DBBASE.metadata.bind = engine

    def drop_db():
        """
        drop the test database
        """
        print("DROPPING DB")
        if __current_test_ini_file().endswith("gitlab-ci.ini"):
            return
        db_settings = get_test_options_from_settings(settings)
        launch_cmd(db_settings["drop"])

    request.addfinalizer(drop_db)
    return _connection


@fixture(scope="session")
def content(connection, settings):
    """
    sets up some default content
    """
    from transaction import commit
    from endi_base.models.base import (
        DBBASE,
    )

    metadata = DBBASE.metadata

    metadata.drop_all(connection.engine)
    from endi.models import adjust_for_engine

    adjust_for_engine(connection.engine)
    metadata.create_all(connection.engine)

    from endi.models.config import Config

    Config.set("invoice_number_template", "{SEQYEAR}")
    Config.set("internalinvoice_number_template", "FI-{SEQYEAR}")
    Config.set("internalsupplierinvoice_number_template", "FRNS-I-{SEQGLOBAL}")
    Config.set("supplierinvoice_number_template", "{SEQGLOBAL}")

    Config.set("expensesheet_number_template", "{SEQGLOBAL}")

    commit()


@fixture
def dbsession(config, content, connection, request):
    """returns a db session object and sets up a db transaction
    savepoint, which will be rolled back after the test.

    :returns: a SQLA session
    """
    from endi import enable_sqla_listeners
    from transaction import abort

    trans = connection.begin()  # begin a non-orm transaction

    def rollback():
        trans.rollback()
        abort()

    request.addfinalizer(rollback)

    enable_sqla_listeners()

    from endi_base.models.base import DBSESSION

    return DBSESSION()


@fixture
def get_raw_request(config, dbsession, registry, settings):
    """
    Build a testing raw request using the Pyramid Request class

    Used for rest views

    Allows to pass a raw request body instead of passing directly parsed params

    :param str request_body: The request body (usefull to validate possible
    datas encoding problems, e.g for rest api calls made from a windows
    server) : the request body is parsed with the json library after being
    decoded, sometimes it gets wrong
    """

    def func(request_body, method="POST", environ=None):
        if environ is None:
            environ = {"REQUEST_METHOD": method}
        from pyramid.request import Request

        request = Request(environ=environ)
        request.body = request_body
        request.context = None
        request.dbsession = dbsession
        request.session = BeakerSessionFactoryConfig()(request)
        return request

    return func


def setup_pyramid_layout(pyramid_request, context):
    print("Adding a pyramid layout")
    from pyramid_layout.layout import LayoutManager

    if context:
        pyramid_request.context = context
    pyramid_request.layout_manager = LayoutManager(context, pyramid_request)


@fixture
def get_csrf_request(config, pyramid_request):
    """
    Build a testing request builder with a csrf token

    :returns: a function to be called with params/cookies/post optionnal
    arguments
    """

    def func(
        params=None,
        cookies=None,
        post=None,
        current_route_name=None,
        current_route_path=None,
        context=None,
        user=None,
        request_config=None,
    ):
        """
        :param dict params: datas passed as request params (GET or POST)
        :param dict cookies: dict of http cookies
        :param dict post: post datas (similar to params but exclusive to POST)
        :param str current_route_name: The current route name (for views with
        redirect)
        :param str current_route_path: The current route name (for views with
        redirect)
        :param obj context: The request's context
        :param obj user: The Current user

        """
        post = post or {}
        if params is not None:
            params.update(post)
        else:
            params = post
        cookies = cookies or {}
        pyramid_request.session = BeakerSessionFactoryConfig()(pyramid_request)
        csrf = pyramid_request.session.get_csrf_token()
        post.update({"csrf_token": csrf})
        pyramid_request.params = params
        pyramid_request.POST = post
        pyramid_request.json_body = post
        pyramid_request.cookies = cookies

        pyramid_request.config = {}
        pyramid_request.registry = config.registry
        pyramid_request.actionmenu = ActionMenu()
        pyramid_request.current_company = None
        pyramid_request.navigation = Navigation()
        pyramid_request.is_popup = False
        if user:
            config.set_security_policy(
                testing.DummySecurityPolicy(
                    identity=user,
                )
            )
        pyramid_request.referer = None
        if context:
            pyramid_request.context = context

        if current_route_path:
            if not current_route_name:
                current_route_name = current_route_path

            route = DummyRoute(name=current_route_name, result=current_route_path)
            mapper = DummyRouteContext(route=route)
            pyramid_request.matched_dict = {}
            pyramid_request.matched_route = route
            pyramid_request.registry.registerUtility(mapper, IRoutesMapper)

        setup_pyramid_layout(pyramid_request, context)

        return pyramid_request

    return func


@fixture
def csrf_request(get_csrf_request):
    return get_csrf_request()


@fixture
def get_csrf_request_with_db(get_csrf_request, pyramid_request, dbsession):
    """
    Build a testing request builder with a csrf token and a db session object

    :returns: a function to be called with params/cookies/post optionnal
    arguments
    """

    def func(*args, **kwargs):
        pyramid_request = get_csrf_request(*args, **kwargs)
        pyramid_request.dbsession = dbsession
        from endi.models.config import get_config

        pyramid_request.config = get_config()
        return pyramid_request

    return func


@fixture
def get_csrf_request_with_db_and_user(get_csrf_request_with_db, user):
    def f(*args, **kwargs):
        kwargs["user"] = user
        req = get_csrf_request_with_db(*args, **kwargs)
        return req

    return f


@fixture
def csrf_request_with_db_and_user(get_csrf_request_with_db_and_user):
    return get_csrf_request_with_db_and_user()


@fixture
def wsgi_app(settings, dbsession):
    from endi import base_configure, prepare_config

    config = prepare_config(**settings)
    return base_configure(
        config, dbsession, from_tests=True, **settings
    ).make_wsgi_app()


@fixture
def app(wsgi_app):
    from webtest import TestApp

    return TestApp(wsgi_app)


# Common Models fixtures
@fixture
def groups(dbsession):
    from endi.models.user.group import Group

    groups = []
    for name in ("contractor", "manager", "admin"):
        group = Group(name=name, label=name, primary=True)
        dbsession.add(group)
        dbsession.flush()
        groups.append(group)

    for name in ("trainer", "constructor"):
        group = Group(name=name, label=name)
        dbsession.add(group)
        dbsession.flush()
        groups.append(group)

    return groups


@fixture
def mk_tva(fixture_factory):
    from endi.models.tva import Tva

    return fixture_factory(Tva, default=False, name="TVA")


@fixture
def tva(tva20):
    return tva20


@fixture
def mk_product(fixture_factory):
    from endi.models.tva import Product

    return fixture_factory(Product, compte_cg="122", name="Product")


@fixture
def product(tva, mk_product):
    return mk_product(name="product", tva=tva)


@fixture
def mk_work_unit(fixture_factory):
    from endi.models.task.unity import WorkUnit

    return fixture_factory(WorkUnit)


@fixture
def unity(mk_work_unit):
    return mk_work_unit(label="h")


@fixture
def mk_task_mention(fixture_factory):
    from endi.models.task.mentions import TaskMention

    return fixture_factory(TaskMention)


@fixture
def mention(mk_task_mention):
    return mk_task_mention(title="TaskMention tet", full_text="blabla", label="bla")


@fixture
def mode(dbsession):
    from endi.models.payments import PaymentMode

    mode = PaymentMode(label="Chèque")
    dbsession.add(mode)
    dbsession.flush()
    return mode


@fixture
def mk_bankaccount(fixture_factory):
    from endi.models.payments import BankAccount

    return fixture_factory(
        BankAccount, label="Banque CAE", code_journal="bq", compte_cg="123"
    )


@fixture
def bank(mk_bankaccount):
    return mk_bankaccount()


@fixture
def mk_bank(fixture_factory):
    from endi.models.payments import Bank

    return fixture_factory(Bank, label="Banque client")


@fixture
def customer_bank(mk_bank):
    return mk_bank()


@fixture
def mk_user(fixture_factory):
    from endi.models.user.user import User

    return fixture_factory(
        User,
        email="default@mail.fr",
        lastname="Lastname",
        firstname="Firstname",
    )


@fixture
def user(mk_user):
    return mk_user(
        email="login@c.fr",
        compte_tiers="COMP_TIERS_USER",
    )


@fixture
def user2(mk_user):
    return mk_user()


@fixture
def mk_login(dbsession, mk_user):
    def _mk_login(login, password="pwd", login_user=None):
        if login_user is None:
            login_user = mk_user()
        from endi.models.user.login import Login

        model = Login(login=login, user_id=login_user.id)
        model.set_password(password)
        dbsession.add(model)
        dbsession.flush()
        login_user.login = model
        return model

    return _mk_login


@fixture
def login(mk_login, user):
    return mk_login(login="login", login_user=user)


@fixture
def mk_company(dbsession, user, login):
    def _mk_company(
        name="My company",
        email=None,
        code_compta=None,
        employee=None,
        internal=False,
        **kwargs,
    ):
        from endi.models.company import Company

        company = Company(
            name=name,
            email=email,
            code_compta=code_compta,
            internal=internal,
            **kwargs,
        )
        if employee is None:
            employee = user
        company.employees = [employee]
        dbsession.add(company)
        dbsession.flush()
        user.companies = [company]
        dbsession.merge(user)
        dbsession.flush()
        return company

    return _mk_company


@fixture
def company(mk_company):
    return mk_company(
        name="Company",
        email="company@c.fr",
        code_compta="0USER",
    )


company1 = company


@fixture
def company2(mk_company):
    return mk_company(
        name="Company2",
        email="company2@c.fr",
        code_compta="1USER",
    )


@fixture
def internal_company(mk_company):
    return mk_company(
        name="CAE Company",
        email="companycae@c.fr",
        code_compta="",
        internal=True,
    )


@fixture
def company3(mk_company):
    return mk_company(
        name="Company3",
        email="sophro@behappy.endi",
        code_compta="3USER",
        general_customer_account="00099988",
        third_party_customer_account="00055566",
        general_supplier_account="0002332415",
        third_party_supplier_account="000056565656",
    )


@fixture
def mk_supplier(dbsession, company, fixture_factory):
    from endi.models.third_party.supplier import Supplier

    return fixture_factory(
        Supplier,
        company_name="supplier",
        type="company",
        lastname="Lastname",
        firstname="Firstname",
        address="1th street",
        zip_code="01234",
        city="City",
        company=company,
        registration="12341234",
    )


@fixture
def supplier(mk_supplier):
    return mk_supplier(company_name="Fournisseur Test")


@fixture
def mk_customer(fixture_factory, company):
    from endi.models.third_party.customer import Customer

    return fixture_factory(
        Customer,
        company_name="customer",
        type="company",
        code="CUST",
        lastname="Lastname",
        firstname="Firstname",
        address="1th street",
        zip_code="01234",
        city="City",
        company_id=company.id,
    )


@fixture
def customer(mk_customer, company):
    customer = mk_customer()
    return customer


@fixture
def customer2(mk_customer, company):
    return mk_customer(company_name="customer2")


@fixture
def individual_customer(mk_customer):
    return mk_customer(
        type="individual",
        civilite="mr&mme",
    )


@fixture
def internal_customer(mk_customer, company2):
    return mk_customer(type="internal", company_name="Interne", source_company=company2)


@fixture
def mk_business_type(fixture_factory):
    """
    Return a BusinessType builder

    def test_test(mk_business_type):
        btype = mk_business_type(name="test")
    """
    from endi.models.project.types import BusinessType

    factory = fixture_factory(
        BusinessType,
        bpf_related=False,
    )

    def func(name, label=None, **kwargs):
        label = label or name
        return factory(name=name, label=label, **kwargs)

    return func


@fixture
def default_business_type(dbsession, mk_business_type):
    return mk_business_type(name="default", label="Cycle court")


@fixture
def mk_file_type(fixture_factory):
    """
    Return a BusinessType builder

    def test_test(mk_file_type):
        ftype = mk_file_type(label="File type")
    """
    from endi.models.files import FileType

    return fixture_factory(FileType)


@fixture
def mk_file(fixture_factory, dbsession):
    """
    Return a File object builder

    def test_test(mk_file):
        f = mk_file(label="File")
    """
    from endi.models.files import File

    factory = fixture_factory(File)

    def func(name="filename", parent=None, description="Description", data=b"1234"):
        res = factory(name=name, description=description, parent=parent)
        res.data = data
        dbsession.merge(res)
        return res

    return func


@fixture
def mk_business_type_file_types(dbsession):
    """
    Build a Business - FileType requirement

    file_type

        A previously generated file_type instance

    business_type

        A previously generated business_type instance

    doctype

        business/estimation/invoice/cancelinvoice

    req_type

        project_mandatory/business_mandatory/mandatory/recommended/optionnal

    validation

        Should the file type be validated (default False)


    def test_test(mk_business_type_file_types, mk_business_type, mk_file_type):
        ftype = mk_file_type(label="file type")
        btype = mk_business_type("btype")
        # ftype is mandatory for each invoice inside businesses of type btype
        req = mk_business_type_file_types(ftype, btype, 'invoice', 'mandatory')

    """
    from endi.models.project.file_types import BusinessTypeFileType

    def func(file_type, business_type, doctype, req_type, validation=False):
        model = BusinessTypeFileType(
            file_type_id=file_type.id,
            business_type_id=business_type.id,
            doctype=doctype,
            requirement_type=req_type,
            validation=validation,
        )
        dbsession.add(model)
        dbsession.flush()
        return model

    return func


@fixture
def mk_project_type(dbsession, default_business_type):
    from endi.models.project.types import ProjectType

    def func(
        name,
        label=None,
        default_btype=default_business_type,
        other_business_types=[],
        with_business=False,
        **kwargs,
    ):
        if label is None:
            label = name
        if not hasattr(other_business_types, "__iter__"):
            other_business_types = [other_business_types]
        params = dict(name=name, label=label, with_business=with_business)
        params.update(kwargs)
        ptype = ProjectType(**params)
        ptype.default_business_type = default_btype
        ptype.other_business_types = other_business_types
        dbsession.add(ptype)
        dbsession.flush()
        default_btype.project_type = ptype
        return ptype

    return func


@fixture
def project_type(dbsession, mk_business_type, mk_project_type):
    ptype = mk_project_type(
        name="default",
        label="Par défaut",
        other_business_types=mk_business_type(name="other", label="Cycle long"),
    )
    return ptype


@fixture
def mk_project(dbsession, company, customer, project_type):
    """
    Return a project builder tool

    name

        Name of the project

    company

        Company owning the project

    customers

        Project is associated to the given customers

    project_type

        Which project type is this project associated to ?
    """
    from endi.models.project import Project

    def func(
        name="Project",
        company=company,
        customers=[customer],
        project_type=project_type,
    ):
        if not hasattr(customers, "__iter__"):
            customers = [customers]

        project = Project(name="Project", project_type=project_type)
        project.company = company
        project.customers = customers
        dbsession.add(project)
        dbsession.flush()
        return project

    return func


@fixture
def project(mk_project):
    return mk_project()


@fixture
def mk_business(fixture_factory, default_business_type, project):
    from endi.models.project.business import Business

    return fixture_factory(
        Business,
        name="business",
        business_type=default_business_type,
        project=project,
    )


@fixture
def mk_business_with_project_mode_ttc(fixture_factory, default_business_type, project):
    project.mode = "ttc"
    from endi.models.project.business import Business

    return fixture_factory(
        Business,
        name="business",
        business_type=default_business_type,
        project=project,
    )


@fixture
def business(mk_business):
    return mk_business()


@fixture
def business2(mk_business):
    return mk_business()


@fixture
def business_with_project_mode_ttc(mk_business_with_project_mode_ttc):
    return mk_business_with_project_mode_ttc()


@fixture
def training_business_type(mk_business_type):
    return mk_business_type("training", bpf_related=True)


@fixture
def training_business(dbsession, mk_business, training_business_type):
    business = mk_business(business_type=training_business_type)
    dbsession.add(business)
    dbsession.flush()
    return business


@fixture
def mk_phase(fixture_factory):
    from endi.models.project import Phase

    return fixture_factory(Phase)


@fixture
def phase(mk_phase, project):
    return mk_phase(name="Phase", project=project)


@fixture
def cae_situation_option(dbsession):
    from endi.models.user.userdatas import (
        CaeSituationOption,
    )

    option = CaeSituationOption(
        is_integration=False,
        label="CaeSituationOption",
    )
    dbsession.add(option)
    dbsession.flush()
    return option


@fixture
def mk_social_status(fixture_factory):
    from endi.models.user.userdatas import SocialStatusOption

    return fixture_factory(SocialStatusOption)


@fixture
def social_status_option1(mk_social_status):
    return mk_social_status(label="Social status 1")


@fixture
def social_status_option2(mk_social_status):
    return mk_social_status(label="Social status 2")


@fixture
def mk_company_activity(fixture_factory):
    from endi.models.company import CompanyActivity

    return fixture_factory(CompanyActivity, label="arts / peintures")


@fixture
def mk_task_insurance_option(fixture_factory):
    from endi.models.task.insurance import TaskInsuranceOption

    return fixture_factory(TaskInsuranceOption, label="Taux d'assurance", rate=10)


@fixture
def task_insurance_option(mk_task_insurance_option):
    return mk_task_insurance_option()


@fixture
def userdatas(dbsession, user, cae_situation_option, carreer_path):
    from endi.models.user.userdatas import (
        UserDatas,
        CompanyDatas,
    )

    result = UserDatas(
        situation_situation=cae_situation_option,
        coordonnees_lastname="Userdatas",
        coordonnees_firstname="userdatas",
        coordonnees_email1="userdatas@test.fr",
        activity_companydatas=[
            CompanyDatas(
                title="test enseigne",
                name="test enseigne",
            )
        ],
        user_id=user.id,
        career_paths=[carreer_path],
    )
    result.situation_situation_id = cae_situation_option.id
    dbsession.add(result)
    dbsession.flush()
    user.userdatas = result
    return result


@fixture
def carreer_path(dbsession):
    from endi.models.career_path import CareerPath

    cp = CareerPath(
        start_date="2019-02-25",
        stage_type="amendment",
        taux_horaire=24.00,
        num_hours=151.00,
        hourly_rate_string="Vingt quatre euros",
        parcours_salary=3624.00,
    )
    dbsession.add(cp)
    dbsession.flush()
    return cp


@fixture
def social_doctypes(dbsession):
    from endi.models.user.userdatas import SocialDocTypeOption

    options = []
    for i in "Rib", "Permis":
        option = SocialDocTypeOption(label=i)
        dbsession.add(option)
        dbsession.flush()
        options.append(option)
    return options


@fixture
def mk_expense_line(fixture_factory, expense_type):
    from endi.models.expense.sheet import ExpenseLine

    return fixture_factory(
        ExpenseLine,
        category="2",
        type_id=expense_type.id,
        ht=10000,
        tva=2000,
    )


@fixture
def mk_expense_kmline(fixture_factory, expense_type_km):
    from endi.models.expense.sheet import ExpenseKmLine

    return fixture_factory(
        ExpenseKmLine,
        category="2",
        type_id=expense_type_km.id,
        km=10,
        ht=10 * expense_type_km.amount,
    )


@fixture
def mk_expense_type(dbsession):
    from endi.models.expense.types import (
        ExpenseKmType,
        ExpenseTelType,
        ExpenseType,
    )

    def builder(
        label="",
        code="",
        amount=None,
        percentage=None,
        year=2018,
        active=True,
        tva_on_margin=False,
        compte_produit_tva_on_margin="7123456",
        code_tva="",
        compte_tva="",
        contribution=False,
        internal=False,
    ):
        args = dict(
            label=label,
            code=code,
            active=active,
            tva_on_margin=tva_on_margin,
            contribution=contribution,
            code_tva=code_tva,
            compte_tva=compte_tva,
            compte_produit_tva_on_margin=compte_produit_tva_on_margin,
            internal=internal,
        )
        if amount is not None:
            factory = ExpenseKmType
            args.update(dict(amount=amount, year=year))

        elif percentage is not None:
            factory = ExpenseTelType
            args.update(dict(percentage=percentage))

        else:
            factory = ExpenseType

        typ = factory(**args)
        dbsession.add(typ)
        dbsession.flush()
        return typ

    return builder


@fixture
def expense_type(mk_expense_type):
    return mk_expense_type(label="Base type")


@fixture
def expense_type_tva_on_margin(mk_expense_type):
    return mk_expense_type(
        tva_on_margin=True,
        compte_produit_tva_on_margin="CG_TVA_OM",
        code="ETYPETVAOM",
    )


@fixture
def expense_type_km(mk_expense_type):
    return mk_expense_type(
        label="Km type",
        amount=1,
    )


@fixture
def expense_type_tel_50(mk_expense_type):
    return mk_expense_type(
        label="Tel type 50%",
        percentage=50,
    )


@fixture
def mk_expense_sheet(fixture_factory, user, company):
    from endi.models.expense.sheet import ExpenseSheet

    return fixture_factory(
        ExpenseSheet,
        month=10,
        year=2015,
        title="Titre NDD",
        company_id=company.id,
        user_id=user.id,
    )


@fixture
def expense_sheet(mk_expense_sheet):
    return mk_expense_sheet()


@fixture
def mk_supplier_order(company, supplier, fixture_factory):
    from endi.models.supply import SupplierOrder

    return fixture_factory(
        SupplierOrder,
        company_id=company.id,
        supplier_id=supplier.id,
    )


@fixture
def supplier_order(mk_supplier_order):
    return mk_supplier_order()


@fixture
def invoiced_supplier_order(mk_supplier_order, supplier_invoice):
    return mk_supplier_order(
        supplier_invoice_id=supplier_invoice.id,
        status="valid",
    )


@fixture
def mk_supplier_invoice(company, supplier, fixture_factory):
    from endi.models.supply import SupplierInvoice

    return fixture_factory(
        SupplierInvoice,
        company_id=company.id,
        supplier_id=supplier.id,
    )


@fixture
def supplier_invoice(mk_supplier_invoice):
    return mk_supplier_invoice()


@fixture
def mk_supplier_invoice_line(fixture_factory):
    from endi.models.supply import SupplierInvoiceLine

    return fixture_factory(
        SupplierInvoiceLine,
    )


@fixture
def half_cae_supplier_invoice(
    dbsession,
    expense_type,
    mk_supplier_invoice,
    mk_supplier_invoice_line,
    user,
    business,
    customer,
):
    # Total TTC : 11.03 ; 50/50 CAE/ES
    inv = mk_supplier_invoice(
        cae_percentage=50,
        payer=user,
    )
    line1 = mk_supplier_invoice_line(
        ht=1000,
        tva=99,
        supplier_invoice=inv,
        expense_type=expense_type,
        business_id=business.id,
        project_id=business.project_id,
        customer_id=customer.id,
    )
    line2 = mk_supplier_invoice_line(
        ht=3,
        tva=1,
        supplier_invoice=inv,
        expense_type=expense_type,
    )
    inv.lines = [line1, line2]
    dbsession.merge(inv)
    dbsession.flush()
    return inv


@fixture
def mk_supplier_order_line(fixture_factory):
    from endi.models.supply import SupplierOrderLine

    return fixture_factory(
        SupplierOrderLine,
    )


@fixture
def mk_sale_product_work(dbsession, fixture_factory, company):
    opts = {"label": "Label", "company_id": company.id}
    from endi.models.sale_product.work import SaleProductWork

    return fixture_factory(SaleProductWork, **opts)


@fixture
def training_type_option(mk_training_type_option):
    return mk_training_type_option()


@fixture
def mk_training_type_option(fixture_factory):
    from endi.models.sale_product.training import TrainingTypeOptions

    return fixture_factory(TrainingTypeOptions, label="Bilan de compétence")


@fixture
def sale_product_training(mk_sale_product_training, training_type_option):
    return mk_sale_product_training(types=[training_type_option])


@fixture
def mk_sale_product_training(fixture_factory, company):
    opts = {"label": "Label", "company_id": company.id}
    from endi.models.sale_product.training import SaleProductTraining

    return fixture_factory(
        SaleProductTraining,
        label="Label Training",
        company_id=company.id,
    )


@fixture
def sale_product_work(mk_sale_product_work):
    return mk_sale_product_work(title="Work", description="Product work")


@fixture
def mk_sale_product(dbsession, fixture_factory, company, tva, product):
    from endi.models.sale_product.sale_product import SaleProductMaterial

    opts = {
        "label": "Label",
        "company_id": company.id,
        "tva_id": tva.id,
        "product_id": product.id,
    }
    return fixture_factory(SaleProductMaterial, **opts)


@fixture
def mk_sale_product_category(fixture_factory):
    from endi.models.sale_product.category import SaleProductCategory

    return fixture_factory(
        SaleProductCategory,
        title="My Cat Title",
        description="My Category Desc",
    )


@fixture
def sale_product_category(mk_sale_product_category, company):
    return mk_sale_product_category(company_id=company.id)


@fixture
def sale_product(mk_sale_product):
    res = mk_sale_product(supplier_ht=100000)
    res.sync_amounts()
    return res


@fixture
def mk_sale_product_work_item(dbsession, fixture_factory, sale_product):
    from endi.models.sale_product.work_item import WorkItem

    opts = {"type_": "material", "base_sale_product_id": sale_product.id}
    return fixture_factory(WorkItem, **opts)


@fixture
def mk_price_study(dbsession, fixture_factory, estimation):
    opts = {"task": estimation}
    from endi.models.price_study import PriceStudy

    return fixture_factory(PriceStudy, **opts)


@fixture
def price_study(mk_price_study):
    return mk_price_study()


@fixture
def mk_price_study_chapter(fixture_factory, price_study):
    from endi.models.price_study import PriceStudyChapter

    return fixture_factory(
        PriceStudyChapter,
        price_study=price_study,
        title="Chapter",
        description="Chapter one",
    )


@fixture
def price_study_chapter(mk_price_study_chapter):
    return mk_price_study_chapter()


@fixture
def mk_price_study_product(price_study_chapter, fixture_factory):
    from endi.models.price_study.product import PriceStudyProduct

    opts = {"chapter_id": price_study_chapter.id}
    return fixture_factory(PriceStudyProduct, **opts)


@fixture
def mk_price_study_work(dbsession, company, price_study_chapter, fixture_factory, tva):
    from endi.models.price_study.work import PriceStudyWork

    opts = {
        "chapter_id": price_study_chapter.id,
        "title": "Title",
        "quantity": 1,
        "tva": tva,
    }
    return fixture_factory(PriceStudyWork, **opts)


@fixture
def price_study_work(mk_price_study_work):
    return mk_price_study_work()


@fixture
def mk_price_study_work_item(dbsession, company, price_study_work, fixture_factory):
    from endi.models.price_study.work_item import PriceStudyWorkItem

    opts = {
        "ht": 100000,
        "price_study_work_id": price_study_work.id,
    }
    return fixture_factory(PriceStudyWorkItem, **opts)


@fixture
def mk_price_study_discount(dbsession, company, price_study, fixture_factory):
    from endi.models.price_study.discount import PriceStudyDiscount

    opts = {"price_study_id": price_study.id}
    return fixture_factory(PriceStudyDiscount, **opts)


@fixture
def mk_bank_remittance(bank, fixture_factory):
    from endi.models.task.payment import BankRemittance

    return fixture_factory(BankRemittance, bank_id=bank.id)


@fixture
def mk_config(dbsession):
    def factory(key, value):
        from endi.models.config import Config

        Config.set(key, value)

    return factory


@fixture
def product_without_tva(dbsession):
    from endi.models.tva import Product

    product = Product(name="product", compte_cg="122")
    dbsession.add(product)
    dbsession.flush()
    return product


@fixture
def mk_task_line_group(fixture_factory):
    from endi.models.task.task import TaskLineGroup

    return fixture_factory(
        TaskLineGroup,
        order=1,
        title="Group title",
        description="Group description",
    )


@fixture
def task_line_group(mk_task_line_group):
    return mk_task_line_group()


@fixture
def mk_task_line(
    fixture_factory,
    unity,
    tva,
    product,
    task_line_group,
):
    from endi.models.task.task import TaskLine

    # TTC = 120 €
    return fixture_factory(
        TaskLine,
        description="Default description",
        cost=10000000,
        quantity=1,
        unity=unity.label,
        tva=tva.value,
        product_id=product.id,
        group=task_line_group,
    )


@fixture
def task_line(mk_task_line):
    return mk_task_line()


@fixture
def bank_remittance(mk_bank_remittance):
    return mk_bank_remittance(id="REM_ID")


@fixture
def mk_payment(invoice, bank, tva, user, customer_bank, fixture_factory):
    from endi.models.task.payment import Payment

    return fixture_factory(
        Payment,
        task_id=invoice.id,
        bank_id=bank.id,
        tva_id=tva.id,
        user_id=user.id,
        customer_bank_id=customer_bank.id,
        task=invoice,
        issuer=invoice.customer.label,
    )


@fixture
def mk_internalpayment(internalinvoice, fixture_factory):
    from endi.models.task.internalpayment import InternalPayment

    return fixture_factory(
        InternalPayment,
        task=internalinvoice,
        amount=10000000,
        date=datetime.datetime.now(),
    )


@fixture
def internalpayment(mk_internalpayment):
    return mk_internalpayment()


@fixture
def internal_product(mk_tva, mk_product):
    tva = mk_tva(name="test", value=0)
    product = mk_product(
        tva=tva,
        name="interne",
        internal=True,
        compte_cg="70400000",
    )
    return product


@fixture
def mk_discount_line(fixture_factory, tva):
    from endi.models.task.task import DiscountLine

    return fixture_factory(
        DiscountLine,
        description="Discount",
        amount=1000000,
        tva=tva.value,
    )


@fixture
def mk_post_ttc_line(fixture_factory):
    from endi.models.task.task import PostTTCLine

    return fixture_factory(
        PostTTCLine,
        label="Remise Post-TTC",
        amount=-5000000,
    )


@fixture
def payment(bank_remittance, mk_payment):
    return mk_payment(amount=1000000, bank_remittance_id="REM_ID", exported=1)


@fixture
def discount_line(mk_discount_line):
    return mk_discount_line()


@fixture
def mk_payment_line(fixture_factory):
    from endi.models.task.estimation import PaymentLine

    return fixture_factory(PaymentLine, description="Paiement")


@fixture
def payment_line(mk_payment_line):
    return mk_payment_line(amount=2000000)


@fixture
def payment_line2(mk_payment_line):
    return mk_payment_line(amount=10000000)


@fixture
def mk_estimation(
    fixture_factory,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
    default_business_type,
):
    from endi.models.task.estimation import Estimation

    return fixture_factory(
        Estimation,
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
        business_type=default_business_type,
    )


@fixture
def estimation(mk_estimation):
    return mk_estimation()


@fixture
def mk_internalestimation(
    fixture_factory,
    tva,
    unity,
    project,
    internal_customer,
    company,
    user,
    phase,
    default_business_type,
):
    from endi.models.task import InternalEstimation

    return fixture_factory(
        InternalEstimation,
        company=company,
        project=project,
        customer=internal_customer,
        phase=phase,
        user=user,
        business_type=default_business_type,
    )


@fixture
def mk_invoice(
    fixture_factory,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
    default_business_type,
):
    from endi.models.task.invoice import Invoice

    return fixture_factory(
        Invoice,
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
        business_type=default_business_type,
    )


@fixture
def mk_internalinvoice(
    fixture_factory,
    tva,
    unity,
    project,
    internal_customer,
    company,
    user,
    phase,
    default_business_type,
):
    from endi.models.task import InternalInvoice

    return fixture_factory(
        InternalInvoice,
        company=company,
        project=project,
        customer=internal_customer,
        phase=phase,
        user=user,
        business_type=default_business_type,
    )


@fixture
def internalinvoice(mk_internalinvoice):
    return mk_internalinvoice()


@fixture
def invoice(mk_invoice):
    return mk_invoice()


@fixture
def mk_cancelinvoice(
    fixture_factory,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
    default_business_type,
):
    from endi.models.task.invoice import CancelInvoice

    return fixture_factory(
        CancelInvoice,
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
        business_type=default_business_type,
    )


@fixture
def mk_internalcancelinvoice(
    fixture_factory,
    tva,
    unity,
    project,
    internal_customer,
    company,
    user,
    phase,
    default_business_type,
    internalinvoice,
):
    from endi.models.task import InternalCancelInvoice

    return fixture_factory(
        InternalCancelInvoice,
        company=company,
        project=project,
        customer=internal_customer,
        phase=phase,
        user=user,
        business_type=default_business_type,
        invoice=internalinvoice,
    )


@fixture
def internalcancelinvoice(mk_internalcancelinvoice):
    return mk_internalcancelinvoice()


@fixture
def cancelinvoice(mk_cancelinvoice):
    return mk_cancelinvoice()


@fixture
def full_estimation(
    dbsession,
    estimation,
    task_line_group,
    task_line,
    user,
    mention,
    discount_line,
    payment_line,
    payment_line2,
    date_20190101,
    mk_business_type,
):
    # TTC  : 120 - 12  + 12 €
    estimation.description = "Description"
    estimation.paymentDisplay = "SUMMARY"
    estimation.payment_conditions = "Test"
    task_line_group.lines = [task_line]
    estimation.business_type = mk_business_type(name="default")
    estimation.deposit = 10
    estimation.line_groups = [task_line_group]
    estimation.discounts = [discount_line]
    estimation.payment_lines = [payment_line, payment_line2]
    estimation.workplace = "workplace"
    estimation.mentions = [mention]
    estimation.expenses_ht = 1000000
    estimation.validity_duration = "3 mois"
    estimation.start_date = date_20190101
    estimation = dbsession.merge(estimation)
    estimation.cache_totals()
    dbsession.flush()
    return estimation


@fixture
def full_invoice(
    dbsession,
    invoice,
    task_line_group,
    task_line,
    user,
    mention,
    discount_line,
    date_20190101,
):
    # TTC  : 120 - 12  + 12 €
    task_line_group.lines = [task_line]
    invoice.line_groups = [task_line_group]
    invoice.discounts = [discount_line]
    invoice.workplace = "workplace"
    invoice.mentions = [mention]
    invoice.expenses_ht = 1000000
    invoice.description = "Description"
    invoice.payment_conditions = "Test"
    invoice.start_date = date_20190101
    invoice = dbsession.merge(invoice)
    invoice.cache_totals()
    dbsession.flush()
    return invoice


@fixture
def mk_full_invoice(
    date_20190101, dbsession, mk_invoice, mk_task_line, mk_task_line_group
):
    def _mk_full_invoice(**kwargs):
        group = mk_task_line_group()
        inv = mk_invoice(year=2019, **kwargs)
        inv.lines = [mk_task_line(date=date_20190101, group=group)]
        inv.line_groups = [group]
        inv = dbsession.merge(inv)
        inv.cache_totals()
        dbsession.flush()
        return inv

    return _mk_full_invoice


@fixture
def draft_invoice(mk_full_invoice):
    return mk_full_invoice(financial_year=2019, status="draft")


@fixture
def unpaid_invoice(mk_full_invoice):
    return mk_full_invoice(
        financial_year=2019,
        status="valid",
        paid_status="waiting",
    )


@fixture
def mk_fully_paid_invoice(
    date_20190101,
    dbsession,
    discount_line,
    mk_full_invoice,
    bank_remittance,
    mk_payment,
):
    def _mk_fully_paid_invoice(with_discount=False, **kwargs):
        kwargs_with_defaults = dict(
            financial_year=2019,
            status="valid",
        )
        kwargs_with_defaults.update(kwargs)
        inv = mk_full_invoice(**kwargs_with_defaults)
        if with_discount:
            # 10€HT 12€TTC
            inv.discounts = [discount_line]
            payment_amount = inv.ttc - discount_line.total()
        else:
            payment_amount = inv.ttc

        payment = mk_payment(
            amount=payment_amount,
            bank_remittance_id="REM_ID",
            exported=1,
            date=date_20190101,
        )
        inv.payments = [payment]
        inv = dbsession.merge(inv)
        inv.check_resulted()
        assert inv.paid_status == "resulted"
        dbsession.flush()
        return inv

    return _mk_fully_paid_invoice


@fixture
def fully_paid_invoice(mk_fully_paid_invoice):
    return mk_fully_paid_invoice()


@fixture
def mk_progress_invoicing_chapter_status(fixture_factory):
    from endi.models.progress_invoicing import ProgressInvoicingChapterStatus

    return fixture_factory(
        ProgressInvoicingChapterStatus,
    )


@fixture
def progress_invoicing_chapter_status(
    mk_progress_invoicing_chapter_status, task_line_group
):
    return mk_progress_invoicing_chapter_status(source_task_line_group=task_line_group)


@fixture
def mk_progress_invoicing_product_status(
    fixture_factory, progress_invoicing_chapter_status
):
    from endi.models.progress_invoicing import ProgressInvoicingProductStatus

    return fixture_factory(
        ProgressInvoicingProductStatus,
        percent_to_invoice=100,
        percent_left=100,
        chapter_status=progress_invoicing_chapter_status,
    )


@fixture
def progress_invoicing_product_status(mk_progress_invoicing_product_status, task_line):
    return mk_progress_invoicing_product_status(source_task_line=task_line)


@fixture
def mk_progress_invoicing_work_status(
    fixture_factory,
    progress_invoicing_chapter_status,
):
    from endi.models.progress_invoicing import ProgressInvoicingWorkStatus

    return fixture_factory(
        ProgressInvoicingWorkStatus,
        percent_to_invoice=100,
        percent_left=100,
        chapter_status=progress_invoicing_chapter_status,
    )


@fixture
def progress_invoicing_work_status(mk_progress_invoicing_work_status, task_line):
    return mk_progress_invoicing_work_status(source_task_line=task_line)


@fixture
def mk_progress_invoicing_work_item_status(
    fixture_factory,
    progress_invoicing_work_status,
):
    from endi.models.progress_invoicing import ProgressInvoicingWorkItemStatus

    return fixture_factory(
        ProgressInvoicingWorkItemStatus,
        percent_to_invoice=100,
        percent_left=100,
        work_status=progress_invoicing_work_status,
    )


@fixture
def progress_invoicing_work_item_status(
    mk_progress_invoicing_work_item_status,
    mk_price_study_work_item,
):
    ps_work_item = mk_price_study_work_item(ht=100000)
    return mk_progress_invoicing_work_item_status(
        price_study_work_item=ps_work_item,
    )


@fixture
def mk_progress_invoicing_line(fixture_factory, progress_invoicing_line_status):
    from endi.models.progress_invoicing import ProgressInvoicingLine

    return fixture_factory(
        ProgressInvoicingLine, base_status_id=progress_invoicing_line_status.id
    )


@fixture
def mk_progress_invoicing_group(fixture_factory, progress_invoicing_group_status):
    from endi.models.progress_invoicing import ProgressInvoicingGroup

    return fixture_factory(
        ProgressInvoicingGroup,
        base_status_id=progress_invoicing_group_status.id,
    )


@fixture
def progress_business(dbsession, mk_business, full_estimation, default_business_type):
    """
    Build and populate a business in progress invoicing_mode
    """
    business = mk_business(invoicing_mode="progress")
    business.estimations = [full_estimation]
    dbsession.merge(business)
    full_estimation.status = "valid"
    full_estimation.business_type_id = default_business_type.id
    full_estimation.businesses = [business]
    dbsession.merge(full_estimation)
    dbsession.flush()
    business.set_progress_invoicing_mode()
    dbsession.merge(business)
    dbsession.flush()
    return business


@fixture
def progress_invoice(get_csrf_request_with_db, dbsession, progress_business, user):
    """
    Invoice with 10% progress
    """
    invoice = progress_business.add_progress_invoicing_invoice(
        get_csrf_request_with_db(), user
    )
    # On construit la structure de données attendues pour la génération des
    # lignes de prestation
    appstruct = {}
    for status in progress_business.progress_invoicing_group_statuses:
        appstruct[status.id] = {}
        for line_status in status.line_statuses:
            appstruct[status.id][line_status.id] = 10
    # On populate notre facture
    progress_business.populate_progress_invoicing_lines(
        invoice,
        appstruct,
    )
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@fixture
def training_speciality(dbsession):
    from endi.models.training.bpf import NSFTrainingSpecialityOption

    ts = NSFTrainingSpecialityOption(label="114 - Mathématiques")
    dbsession.add(ts)
    dbsession.flush()
    return ts


@fixture
def mk_business_bpf_data(dbsession, training_speciality):
    def _mk_business_bpf_data(
        business,
        financial_year,
        cerfa_version="10443*15",
        training_goal_id=0,
        is_subcontract=False,
    ):
        from endi.models.training.bpf import BusinessBPFData

        bpf_data = BusinessBPFData(
            business_id=business.id,
            financial_year=financial_year,
            cerfa_version=cerfa_version,
            total_hours=100,
            headcount=10,
            has_subcontract="no",
            has_subcontract_hours=0,
            has_subcontract_headcount=0,
            is_subcontract=is_subcontract,
            training_speciality_id=training_speciality.id,
            training_goal_id=training_goal_id,
        )
        dbsession.add(bpf_data)
        dbsession.flush()
        dbsession.refresh(business)
        return bpf_data

    return _mk_business_bpf_data


@fixture
def def_tva(tva):
    return tva


@fixture
def tva10(mk_tva):
    return mk_tva(
        value=1000,
        name="tva 10%",
        compte_cg="TVA10",
        code="CTVA10",
    )


@fixture
def tva20(mk_tva):
    return mk_tva(
        value=2000,
        name="tva 20%",
        compte_cg="TVA20",
        code="CTVA20",
        default=True,
    )


@fixture
def tva55(mk_tva):
    return mk_tva(
        value=550,
        name="tva 5.5%",
        compte_cg="TVA55",
        code="CTVA55",
    )


@fixture
def invoice_ht_mode(mk_invoice):
    return mk_invoice(mode="ht")


@fixture
def mk_internalsupplier_invoice(company, supplier, fixture_factory, internalinvoice):
    from endi.models.supply import InternalSupplierInvoice

    return fixture_factory(
        InternalSupplierInvoice,
        company=company,
        supplier=supplier,
        source_invoice=internalinvoice,
    )


@fixture
def internalsupplier_invoice(mk_internalsupplier_invoice):
    return mk_internalsupplier_invoice()


@fixture
def mk_supplier_payment(fixture_factory, bank, supplier_invoice):
    from endi.models.supply.payment import SupplierInvoiceSupplierPayment

    return fixture_factory(
        SupplierInvoiceSupplierPayment,
        bank_remittance_id="Libelle",
        date=datetime.date(2021, 3, 18),
        amount=100000000,  # 1000€
        bank=bank,
        bank_id=bank.id,
        supplier_invoice=supplier_invoice,
    )


@fixture
def mk_user_payment(fixture_factory, bank, supplier_invoice):
    from endi.models.supply.payment import SupplierInvoiceUserPayment

    return fixture_factory(
        SupplierInvoiceUserPayment,
        bank_remittance_id="Libelle",
        date=datetime.date(2021, 3, 18),
        amount=100000000,  # 1000€
        bank=bank,
        bank_id=bank.id,
        supplier_invoice=supplier_invoice,
    )


@fixture
def mk_internalsupplier_payment(fixture_factory, internalsupplier_invoice):
    from endi.models.supply.internalpayment import (
        InternalSupplierInvoiceSupplierPayment,
    )

    return fixture_factory(
        InternalSupplierInvoiceSupplierPayment,
        date=datetime.date(2021, 3, 18),
        amount=100000000,  # 1000€
        supplier_invoice=internalsupplier_invoice,
    )


@fixture
def mk_custom_invoice_book_entry_module(fixture_factory):
    from endi.models.accounting.bookeeping import CustomInvoiceBookEntryModule

    return fixture_factory(
        CustomInvoiceBookEntryModule,
        doctype="invoice",
        active=True,
        enabled=True,
        title="Custom invoice book entry module",
        compte_cg_credit="CG_IN",
        compte_cg_debit="CG_OUT",
        percentage=1,
        label_template="Custom",
    )


@fixture
def mk_form_field_definition(fixture_factory):
    from endi.models.form_options import FormFieldDefinition

    return fixture_factory(
        FormFieldDefinition,
        form="task",
        visible=True,
    )


@fixture
def app_config(dbsession):
    result = {
        "sage_rginterne": "1",
        "code_journal": "CODE_JOURNAL",
        "cae_general_customer_account": "CAE_CG_CUSTOMER",
        "compte_rrr": "CG_RRR",
        "compte_frais_annexes": "CG_FA",
        "compte_rg_externe": "CG_RG_EXT",
        "compte_rg_interne": "CG_RG_INT",
        "compte_cg_banque": "BANK_CG",
        "compte_cg_tva_rrr": "CG_TVA_RRR",
        "code_tva_rrr": "CODE_TVA_RRR",
        "numero_analytique": "NUM_ANA",
        "rg_coop": "CG_RG_COOP",
        "taux_rg_interne": "5",
        "taux_rg_client": "5",
        "compte_cg_ndf": "CGNDF",
        "code_journal_ndf": "JOURNALNDF",
        "code_journal_waiver_ndf": "JOURNAL_ABANDON",
        "code_tva_ndf": "TVANDF",
        "compte_cg_waiver_ndf": "COMPTE_CG_WAIVER",
        "receipts_active_tva_module": "1",
        "receipts_code_journal": "JOURNAL_RECEIPTS",
        "bookentry_facturation_label_template": (
            "{invoice.customer.label} {company.name}"
        ),
        "bookentry_rg_interne_label_template": (
            "RG COOP {invoice.customer.label} {company.name}"
        ),
        "bookentry_rg_client_label_template": (
            "RG {invoice.customer.label} {company.name}"
        ),
        "bookentry_expense_label_template": (
            "{beneficiaire}/frais {expense_date:%-m %Y}"
        ),
        "bookentry_payment_label_template": (
            "{company.name} / Rgt {invoice.customer.label}"
        ),
        "bookentry_expense_payment_main_label_template": (
            "{beneficiaire_LASTNAME} / REMB FRAIS {expense_date:%B/%Y}"
        ),
        "bookentry_expense_payment_waiver_label_template": (
            "Abandon de créance {beneficiaire_LASTNAME} {expense_date:%B/%Y}"
        ),
        "bookentry_supplier_invoice_label_template": (
            "{company.name} / Fact. {supplier.label}"
        ),
        "bookentry_supplier_payment_label_template": (
            "{company.name} / Rgt {supplier.label}"
        ),
        "bookentry_supplier_invoice_user_payment_label_template": (
            "{beneficiaire_LASTNAME} / REMB FACT {supplier_invoice.official_number}"
        ),
        "bookentry_supplier_invoice_user_payment_waiver_label_template": (
            "Abandon de créance {beneficiaire_LASTNAME}"
            " {supplier_invoice.official_number}"
        ),
        "code_journal_frns": "JOURNAL_FRNS",
        "internalcode_journal": "INTERNAL_JOURNAL",
        "internalnumero_analytique": "INTERNAL_NUM_ANA",
        "internalcompte_frais_annexes": "INTERNAL_CG_FA",
        "internalcompte_cg_banque": "INTERNAL_BANK_CG",
        "internalbookentry_facturation_label_template": (
            "{invoice.customer.label} {company.name}"
        ),
        "internalcompte_rrr": "INTERNAL_CG_RRR",
        "internalcae_third_party_customer_account": "CAE_TIERS_INTERNE",
        "internalcae_third_party_supplier_account": "CAE_TIERS_INTERNE_FRN",
        "internalbookentry_payment_label_template": (
            "{company.name} / Rgt Interne {invoice.customer.label}"
        ),
        "internalcode_journal_encaissement": "INTERNAL_JOURNAL_ENCAISSEMENT",
        "internalbank_general_account": "INTERNAL_BANK_CG_ENCAISSEMENT",
        "internalcode_journal_frns": "INTERNAL_FRNS_JOURNAL",
        "internalbookentry_supplier_invoice_label_template": (
            "{company.name} / Fact Interne {supplier.label}"
        ),
        "internalbookentry_supplier_payment_label_template": (
            "{company.name} / Rgt Interne {supplier.label}"
        ),
        "ungroup_supplier_invoices_export": "1",
    }
    from endi.models.config import Config

    for key, value in result.items():
        Config.set(key, value)
    return result


@fixture
def mk_status_log_entry(dbsession, fixture_factory):
    from endi.models.status import StatusLogEntry

    return fixture_factory(StatusLogEntry)


@fixture
def node(dbsession):
    """Minimal node

    (no subclass, does not exist as-is in real-life)
    """
    from endi.models.node import Node

    node = Node()
    dbsession.add(node)
    dbsession.flush()
    return node


@fixture
def income_statement_measure_type_categories(dbsession):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureTypeCategory,
    )

    result = []
    for i in ("Produits", "Achats"):
        cat = IncomeStatementMeasureTypeCategory(label=i)
        dbsession.add(cat)
        result.append(cat)
    dbsession.flush()
    return result


@fixture
def mk_notification_event(fixture_factory):
    from endi.models.notification import NotificationEvent

    return fixture_factory(
        NotificationEvent, key="system:msg", title="Titre", body="Body"
    )


@fixture
def mk_notification_event_type(fixture_factory):
    from endi.models.notification import NotificationEventType

    return fixture_factory(
        NotificationEventType,
        key="system:msg",
        label="Message système",
        default_channel_name="mail",
    )


@fixture
def mk_notification(fixture_factory):
    from endi.models.notification import Notification

    return fixture_factory(Notification, key="system:msg", title="Titre", body="Body")
