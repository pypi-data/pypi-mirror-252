<%inherit file="${context['main_template'].uri}" />

<%block name='actionmenucontent'>
<div class='layout flex main_actions'>
    <div role='group'></div>
    <div role='group'>
        <a class='btn' href='${export_xls_url}' title="Export au format Excel (xls) dans une nouvelle fenêtre" aria-label="Export au format Excel (xls) dans une nouvelle fenêtre">
            ${api.icon('file-excel')} Excel
        </a>
        <a class='btn' href='${export_ods_url}' title="Export au format Open Document (ods) dans une nouvelle fenêtre" aria-label="Export au format Open Document (ods) dans une nouvelle fenêtre">
            ${api.icon('file-spreadsheet')} ODS
        </a>
    </div>
</div>
</%block>

<%block name='content'>

<div>
    <div class="table_container scroll_hor">
        <table class="hover_table">
            <thead>
                <tr>
                   <th scope="col" class="col_text min10" title="Vous trouverez des précisions sur les données affichées en survolant les en-têtes des colonnes">
                        Salarié <span class="icon">${api.icon('question-circle')}</span> 
                        <span class="screen-reader-text">Vous trouverez des précisions sur les données affichées en survolant les en-têtes des colonnes</span>
                    </th>
                    % for y in years:
                        <th scope="col" class="col_number" title="Total des kilomètres validés dans Moogli en ${y}">
                            N<span class="screen-reader-text">om</span>b<span class="screen-reader-text">re de</span>&nbsp;K<span class="screen-reader-text">ilo</span>m<span class="screen-reader-text">ètres</span> <small>${y}</small>
                        </th>
                    % endfor
                </tr>
                <tr class="row_recap">
                    <th class="col_text min10">TOTAL (${len(kms_datas)} salariés)</th>
                    % for y in years:
                        <td class="col_number">
                            ${api.remove_kms_training_zeros(api.format_amount(total_kms[y]))}
                        </td>
                    % endfor
                </tr>
            </thead>
            <tbody>
                % for data in kms_datas:
                    <tr>
                        <th scope="row" class="col_text min10">
                            ${data["user_label"]}
                        </th>
                        % for y in years:
                            <td class="col_number">
                                ${api.remove_kms_training_zeros(api.format_amount(data["user_kms"][y]))}
                            </td>
                        % endfor
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
</div>

</%block>
