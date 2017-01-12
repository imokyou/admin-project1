# coding=utf-8
resetpwd_template = {
    'version': 1.0,
    'subject': '请重置您的密码',
    'to': [],
    'single':
    """
       <table style="width:1200px;margin:0 auto; border-collapse:collapse;color:#333;font-family:Arial;" cellspacing="0" cellpadding="0">
            <thead style="background:#fefff4">
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">说明：<b>{note}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">推广计划：<b>{ad_name}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">广告主：<b>{ader_name}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td width="432" height="45" style="padding-left:38px;font-size:16px;">合作类型：<b>{cooperation_depth}</b></td>
                    <td style="font-size:16px;">销售负责人：<b>{ader_am_name}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;">Categories：<b>{categories}</b></td>
                    <td style="font-size:16px;">结算类型：<b>{settle_mode}</b></td>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">推广单元名称：<b>{offer_id}{unit_name}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td width="432" height="45" style="padding-left:38px;font-size:16px;">Platform：<b>{sys_type}</b></td>
                    <td style="font-size:16px;">Traffic Type：<b>{traffic_type}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td width="432" height="45" style="padding-left:38px;font-size:16px;">效果类型：<b>{settle_type}</b></td>
                    <td style="font-size:16px;">渠道分成比例：<b>{settle_ratio}</b></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">投放国家&接入单价：
                        <div style="display:inline-block;">
                                {country_ad_price}
                        </div>
                    </td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">放出单价：<span style="color:#ff2525"><b>${sell_price}</b></span></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;">
                        <div><span style="display:inline-block;width:157px;margin-bottom:20px;margin-top:22px;">Daily Cap：</span><span style="color:#ff2525"><b>{daily_cap}</b></span></div>
                        <div><span style="display:inline-block;width:157px;margin-bottom:20px;">Monthly Cap：</span><span style="color:#ff2525"><b>{monthly_cap}</b></span></div>
                        <div><span style="display:inline-block;width:157px;margin-bottom:20px;">Totally Cap：</span><span style="color:#ff2525"><b>{totally_cap}</b></span></div>
                        <div style="position:relative"><span style="display:inline-block;width:157px;margin-bottom:20px;">Timezone：</span><b style="position:absolute;width:150%">(GMT+8.00) Beijing, Chongqing, Hong Kong, Urumqi</b></div>
                    </td>
                    <td style="vertical-align:top;padding-top:22px;font-size:16px;">Budget：<span style="color:#ff2525"><b>$ {budget}</b></span></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">投放周期：<span style="color:#ff2525"><b>{start_time}</b></span> 至 <span style="color:#ff2525"><b>{end_time}</b></span></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2"><span style="color:#ff2525"><b>{new_cap_apply}</b></span></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">Preview Url：<a href="{preview_url}" target="_blank" style="color:#333;"><b>{preview_url}</b></a></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">Tracking Url：<a href="{tracking_link}" target="_blank" style="color:#333;"><b>{tracking_link}</b></a></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">素材：<a href="{creative_filepath}" target="_blank" style="color:#015edc;"><b>{creative_name}</b></a></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;vertical-align:top;" colspan="2">
                        <span style="display:inline-block; vertical-align:top;padding-top:11px;padding-right:10px;">流量需求：</span>
                        <div style="display:inline-block; width:474px;background:#f5f5f5;padding:10px 0 10px 30px;margin:5px 0;">
                            <span style="display:inline-block; width:48%;margin-bottom:18px;">Pop Traffic: <i style="{traffic_66_style}"><b>{traffic_66}</b></i></span>
                            <span style="display:inline-block; width:48%;">Adult Traffic: <i style="{traffic_67_style}"><b>{traffic_67}</b></i></span>
                            <span style="display:inline-block; width:48%;margin-bottom:18px;">Push Traffic: <i style="{traffic_68_style}"><b>{traffic_68}</b></i></span>
                            <span style="display:inline-block; width:48%;">Search Traffic: <i style="{traffic_69_style}"><b>{traffic_69}</b></i></span>
                            <span style="display:inline-block; width:48%;margin-bottom:18px;">In-app Traffic: <i style="{traffic_70_style}"><b>{traffic_70}</b></i></span>
                            <span style="display:inline-block; width:48%;">Facebook Traffic: <i style="{traffic_71_style}"><b>{traffic_71}</b></i></span>
                            <span style="display:inline-block; width:48%;margin-bottom:18px;">Wifi Traffic: <i style="{traffic_72_style}"><b>{traffic_72}</b></i></span>
                            <span style="display:inline-block; width:48%;">SMS Traffic: <i style="{traffic_73_style}"><b>{traffic_73}</b></i></span>
                            <span style="display:inline-block; width:48%;">Email Traffic: <i style="{traffic_74_style}"><b>{traffic_74}</b></i></span>
                            <span style="display:inline-block; width:48%;">Redirected Traffic: <i style="{traffic_75_style}"><b>{traffic_75}</b></i></span>

                        </div>
                    </td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">转化流程：<b> {conversion_flow_note}</b><p></p></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">流量规范：<b> {traffic_regulation_note}</b><p></p></td>
                </tr>
                <tr style="border-bottom:1px dotted #b7b7b7;">
                    <td height="45" style="padding-left:38px;font-size:16px;" colspan="2">KPI：<b> {kpi_note}</b><p></p></td>
                </tr>
            </tbody>
        </table>
    """
}