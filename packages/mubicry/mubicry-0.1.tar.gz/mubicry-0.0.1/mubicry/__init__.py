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