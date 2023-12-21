import pandas as pd
import glob as glob
import shutil
import os
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Mm 


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
    df.rename(columns = col_dict,inplace=True)
    for item in ['birth_date','sample_date','report_date','delivery_date']:
        df[item] = df[item].astype('string')
    results = df.to_dict('records')
    return results

def to_doc(info,outdir):
    binpath = os.path.split(os.path.realpath(__file__))[0]
    tpl = DocxTemplate(f'{binpath}/report_template.docx')
    info['ressult_fig'] = InlineImage(tpl, info['ressult_fig'], width=Mm(80))
    tpl.render(info)
    outf = f'{outdir}/{info["sample_no"]}-{info["name"]}.G6PD.report.docx'
    tpl.save(outf)
    print(f'成功生成报告:{outf}')


if __name__ == '__main__':
    infile = input('请拖入文件')
    print('-------------')
    # print(fis)
    infile = infile.strip().strip('"')
    indir = os.path.dirname(infile)
    
    outdir = indir + '/report'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    results = read_info(infile)
    for each in results:
        pngfi = f'{indir}/图谱/{each["name"]}.PNG'
        if not os.path.exists(pngfi):
            print(f'{each["name"]}在“{indir}/图谱/”中不存在图片')
            continue
        else:
            each['ressult_fig'] = pngfi
            to_doc(each,outdir)
