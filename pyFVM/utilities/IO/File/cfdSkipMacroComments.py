def cfdSkipMacroComments(tline):

    trimmedTline = tline.strip()
    
    if "/*" in trimmedTline:
        tline = False
    elif "|" in trimmedTline:
        tline = False
    elif "\*" in trimmedTline:
        tline = False
    elif "*" in trimmedTline: 
        tline = False
    else:
        tline = tline
    return tline