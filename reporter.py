import pandas as pd

import os
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Mm
# import logging.config
import logging
from PyQt6.QtCore import pyqtSignal

logging.config.fileConfig('./config/logging.ini')
logger = logging.getLogger('worker')

def read_info(fi):
    col_dict = {'序号': 'no',
                '新生儿姓名': 'name',
                '性别': 'gender',
                '出生日期': 'birth_date',
                '采血日期': 'sample_date',
                '检测项目': 'project',
                '联系电话': 'telephone',
                '采样医院': 'sample_hospital',
                '寄送日期': 'delivery_date',
                '样本编号': 'sample_no',
                '报告日期': 'report_date',
                '结果': 'results'}
    df = pd.read_excel(fi)
    df.rename(columns=col_dict, inplace=True)
    for item in ['birth_date', 'sample_date', 'report_date', 'delivery_date']:
        df[item] = df[item].astype('string')
    results = df.to_dict('records')
    return results


def to_doc(info, outdir):
    # binpath = os.path.split(os.path.realpath(__file__))[0]
    # tpl = DocxTemplate(f'{binpath}/report_template.docx')
    tpl = DocxTemplate(f'./config/report_template.docx')
    logger.info(tpl)
    info['ressult_fig'] = InlineImage(tpl, info['ressult_fig'], width=Mm(80))
    logger.info(info)
    tpl.render(info)
    outf = f'{outdir}/{info["sample_no"]}-{info["name"]}.G6PD.report.docx'
    tpl.save(outf)
    logger.info(f'成功生成报告:{outf}')


def run_report(infile,outdir):
    binpath = os.path.split(os.path.realpath(__file__))[0]
    # infile = input('请拖入文件')
    infile = infile.strip().strip('"')
    indir = os.path.dirname(infile)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    results = read_info(infile)
    relate_df = pd.read_excel(os.path.join('./G6PD关系/对应关系.xlsx'))
    relate_dict = relate_df.set_index('结果')['对应图片'].to_dict()

    for each in results:
        logger.info(each)

        result = each.get('results')
        logger.info(result)
        pic_name = relate_dict.get(result)
        logger.info(pic_name)

        pngfi = os.path.abspath(os.path.join('.',f'./G6PD关系/{pic_name}'))
        logger.info(pngfi)
        if not os.path.exists(pngfi):
            logger.info(pngfi)
            logger.info(f'{each["results"]}在“./G6PD关系/”中不存在图片')
            continue
        else:
            each['ressult_fig'] = pngfi
            logger.info('2.4-------------')
            to_doc(each, outdir)



