def contains_invaild_char(text):
    for char in text:
        if ('\u1100' <= char <= '\u11FF' or
            '\u3130' <= char <= '\u318F' or
            '\uAC00' <= char <= '\uD7AF'):
            return True
        # 泰语 (Thai)
        elif '\u0E00' <= char <= '\u0E7F':
            return True
        # 越南语 (Vietnamese - Latin with diacritics)
        elif '\u0100' <= char <= '\u017F' or \
             '\u01A0' <= char <= '\u01B0' or \
             '\u1EA0' <= char <= '\u1EF9':
            return True
        # 藏语 (Tibetan)
        elif '\u0F00' <= char <= '\u0FFF':
            return True
        # 葡萄牙语 (Portuguese - Latin with diacritics)
        elif char in 'áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ':
            return True
    return False