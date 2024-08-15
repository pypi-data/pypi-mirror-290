def validation_and_cleaning_national_code(arg):
    
    english_numbers = '0123456789'
    persian_numbers = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}


    if type(arg) == int:

        if len(str(arg)) == 10:
            return str(arg)
        else:
            raise ValueError('[national_code] must be 10 digits.')
        
    elif type(arg) == str:

        if len(arg) == 10:
            result = ''

            for item in arg:
                if item in english_numbers:
                    result += item
                elif item in persian_numbers.keys():
                    for key, value in persian_numbers.items():
                        if item == key:
                            result += value
                else:
                    raise ValueError('[national_code] must be english or persian numbers.')

            return result
        else:
            raise ValueError('[national_code] must be 10 digits.')

    else:
        raise ValueError('[national_code] must be [int] or [str] Type.')






