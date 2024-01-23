def gerar_rotulo(caminho_salvo):
    import os
    try :
        import xlwings as xw
        import win32api
    except :
        os.system('python3 -m pip install xlwings')
        os.system('python -m pip install xlwings')
        os.system('python3 -m pip install win32api')
        os.system('python -m pip install win32api')
        import xlwings as xw
        import win32api
    file = xw.Book(caminho_salvo)
    labelinfo = file.api.SensitivityLabel.CreateLabelInfo()
    labelinfo.AssignmentMethod = 2
    labelinfo.Justification = 'init'
    labelinfo.LabelId = 'b5ae8281-a660-4ab1-b770-60ed6d338d72'
    labelinfo.LabelName = 'PÚBLICA'
    file.api.SensitivityLabel.SetLabel(labelinfo, labelinfo)
    file.save()
    file.close()

def RO(caminho_dbf,caminho_salvar,nome,mes,ano):
    try:
        from dbfread import DBF
        import pandas as pd
    except:
        import os
        os.system('python3 -m pip install pandas')
        os.system('python -m pip install pandas')
        os.system('python3 -m pip install dbfread')
        os.system('python -m pip install dbfread')
        from dbfread import DBF
        import pandas as pd
    import mubicryy as mb
    mes = str(mes)
    dbf = DBF(caminho_dbf, encoding = 'latin1')
    frame = pd.DataFrame(iter(dbf))
    frame_count = len(frame)
    frame = frame._get_numeric_data()
    total = frame.sum()
    total.name = 'Soma'
    frame = frame.append(total.transpose())
    frame.total = frame.loc[frame.index.isin(['Soma'])]
    frame.total.loc[:,'Record_Count'] = [frame_count]
    frame.total.to_excel(caminho_salvar, index = False)
    mb.gerar_rotulo(caminho_salvar)