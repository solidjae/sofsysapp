import pandas as pd
import langid


def keyword_get():
    keyword_file = pd.read_excel(
        "캠페인별 키워드 performance.xlsx",
    )
    keyword_file['keyword'] = keyword_file['keyword'].str.replace(' ','')
    keyword_file = keyword_file.groupby(['keyword']).sum().reset_index()
    keyword_file['ROAS'] = keyword_file['전환금액']/keyword_file['투자금액']
    print(keyword_file)

if __name__=='__main__':
    keyword_get()