import akasha
GENERATE_SQL_TASK = {
    'prompt':'''
        有一資料庫表單={table_name}
        請基於當下時間{current_datetime}, 將用戶的問題={question}
        參考下面之 表格結構&範例資料&欄位說明, 轉為{columns_str}{sql_type}語法並輸出
        "欄位說明"僅是用於選取正確的欄位&篩選條件，不得用於個別之欄位資料處理(ex: 欄位字串分割、比較)
        ''',
    'system_prompt':'''
        只能產生"查詢資料"的sql語法, 禁止回答其他內容, 否則罰你10000元
        ---
        產生的語句必須符合下列範本：
            select [count] [distinct] [top <資料筆數>] [sum] {columns} from {table_name} 
            [where <條件1> and <條件2> and ... and <條件n>]  
            [order by <排序欄位> <ASC/DESC>] 
            [limit <資料筆數>]
        ---
        "select" 和 "{table_name}" 請直接填寫，不得更換
        "{columns}" 可視情況填寫部分，若為全部欄位，則填寫"*"
        []內的內容為選填項目, 可根據問題需求決定是否使用
        <條件>為一個或多個, 以"where"起頭, 並以"and"連接, 目的是用來限縮資料範圍
        <條件>的篩選範圍值需參考範例資料，且符合該欄位的資料型態
        <排序欄位>為一個或多個, 以"order by"起頭，並以"ASC"或"DESC"結尾
        產生的語句僅限包含此範本1次，不得重複
        ---
        語法使用規範：
        1. 嚴禁使用"group by", "having", "join", "union", "insert", "update", "delete", "all"等任一語法，否則罰你10000元
        2. sum：可用於資料型態為數值型的欄位, 且用戶問題中有"加總"的需求, 否則禁止使用
        3. count：可用於用戶問題中有包含"計算筆數"的需求, 否則禁止使用
            使用時須加上"(<欄位名稱>)"，<欄位名稱>限填1個欄位或是"*"，例如"count({count_sample_usage_str})"
        4. distinct：可用於用戶問題中有包含"不重複"的需求, 否則禁止使用，可接1或多個欄位名稱
            若包在count內使用時，distinct 後面限填寫1個欄位名稱，但不可加上"*"，如"count(distinct <column1>)"
        5. limit/top：可用於用戶問題中有包含"前幾名"的需求, 否則禁止使用
            limit適用於MySQL, PostgreSQL, SQLITE, top僅適用於MSSQL, 兩者限擇一使用
        6. "select" 語法僅限出現1次
        '''
}

GENERATE_ANSWER_TASK = {
    'prompt': '''
        請根據資料庫查詢的結果，回答使用者的問題
        ---
        查詢表格：{table_name}
        查詢使用SQL：{sql}
        查詢結果：\n{data}\n
        使用者問題：{question}
        ''',
    'system_prompt':'''
        請完整瀏覽"查詢結果"後，直接針對用戶問題進行回答，禁止回答其他內容
        若回答之數據有經過計算過程，請詳述其計算過程
        有關數值的大小比較結果之論述，請自我檢查是否正確再輸出
        ---
        若使用者問題符合"有幾筆資料"類型之疑問，請先比對"SQL"與"查詢結果"後
        決定採用查詢結果之(資料筆數or資料內容)進行回答
        '''
}

SIMPLIFY_ANSWER_TASK = {
    'prompt': '''
    ''',
    'system_prompt':'''
    '''
}
    