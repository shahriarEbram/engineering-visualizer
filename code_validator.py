import re
import streamlit as st

equipment_name = {
    'D': 'قالب ریخته گری',
    'C': 'قالب ماهیچه',
    'F': 'فیکسچر',
    'G': 'گیج',
    'M': 'ماشین آلات',
    'T': 'ابزار براده برداری',
    'V': 'متفرقه',
    'Q': 'متفرقه خارج از شرکت',
    'R': 'کارخانه آلیاژ سازی'
}

equipment_name_subset = {
    'D': {
        '10': 'LPDC',
        '11': 'DC (Gravity)',
        '12': 'TILT',
        '13': 'HPDC'
    },
    'C': {
        '10': 'واترجکت',
        '11': 'اویل جکت',
        '12': 'پورت دود',
        '13': 'پورت هوا',
        '14': 'پورت دود و هوا',
        '15': 'میل بادامک',
        '16': 'شمع',
        '17': 'TOP CORE',
        '18': 'کانال وسط',
        '19': 'میل بادامک و کانال',
        '20': 'رایزر کور'
    },
    'F': {
        '10': 'شیفت عرضی',
        '11': 'شیفت طولی',
        '12': 'كنترل اندازه محفظه',
        '13': 'حكاكي شماره زني',
        '14': 'برش اره',
        '15': 'سیت و گاید',
        '16': 'حكاكي لیزر',
        '51': 'ماشینکاری op10',
        '52': 'ماشینکاری op20',
        '53': 'ماشینکاری op50',
        '54': 'ماشینکاری OP30',
        '55': 'ماشینکاری OP40',
        '71': 'کلمپ های هیدرولیک چکشی',
        '72': 'کلمپ های هیدرولیک گردشی',
        '73': 'فیکسچر ماشینکاری کیوب',
        '74': 'فیکسچر درپوش',
        '75': 'فیکسچر محفظه',
        '76': 'فیکسچر منیفولد',
        '77': 'فیکسچر جانبی',
        '78': 'فیکسچر شمع',
        '79': 'فیکسچر استکانی',
        '80': 'فیکسچر ماشینکاری لانگبورینگ',
        '81': 'فیکسچرهای ماشین هکرت',
    },
    'G': {
        '10': ' موقعيت كپه',
        '11': 'منيفولد دود',
        '12': 'منيفولد هوا',
        '13': ' لنگي و سيت و گايد',
        '14': 'میز صافی سطح',
        '15': 'مولتی کنترلی استکانی'

    },
    'M': {

        '11': 'ریخته گری DC',
        '12': 'ریخته گری TILT',
        '13': 'واترجکت',
        '14': 'اویل جکت',
        '15': 'پورت دود',
        '16': 'پورت هوا',
        '17': 'پورت دود و هوا',
        '18': 'میل بادامک',
        '19': 'شمع',
        '20': 'کانال وسط',
        '21': 'ماشین کاری',
        '22': 'مخصوص',
        '23': 'تست راکروم',
        '24': 'سواخ آب',
        '25': 'لوپرژر',
        '26': 'کوره ذوب',
        '27': 'کاراسلی',
        '28': 'شات بلاست',
        '29': 'دکورینگ',
        '30': 'کوره عملیات حرارتی',
        '31': 'کوره بازیافت',
        '32': 'دستگاه هم زن',
        '33': 'دستگاه سرند',
        '34': 'tx3000',
        '35': 'دستگاه تست کاسه نمد',
        '36': 'کفتراش',
        '37': 'دستگاه کیوب',
        '38': 'ماشین ماهیچه افقی',
        '39': 'ماشین ماهیچه عمودی',
        '40': 'فاتا',
        '41': 'کوره پخت',
        '42': 'میز ویبره',
        '43': 'دستگاه سیت و گاید سمت دود',
        '44': 'دستگاه سیت و گاید سمت هوا',
        '45': 'نوار نقاله کوره بازیافت',
        '46': 'همزن مذاب(MTS)',
        '47': 'بالابر ماسه(Elevator)',
        '48': 'ماشین ماهیچه کلد باکس',
        '49': 'ماشین تست لیک',
        '50': 'گونیا',
        '51': 'قلاویز',
        '52': 'ماشین آسیاب'
    },
    'T': {
        '10': 'هلدر',
        '11': 'چکش بادی',
        '12': 'مولتی 10 محوره'
    },
    'V': {
        '10': 'مدل قطعه دیوایدر',
        '11': 'مدل مخروطی',
        '12': 'مدل لاست فوم',
        '30': 'طراحی مکانیزم',
        '31': 'عمومی',
        '32': 'فرز',
        '33': 'باکس رنگ',
        '34': 'لیفتراک',
        '35': 'نمونه کشش',
        '36': 'اره',
        '37': 'جانمایی دستگاه ها',
        '38': 'پرینتر 3بعدی',
        '39': 'قالب توری کاپی',
        '40': 'مدل سازی 3بعدی',
        '41': 'جرثقیل',
        '42': 'مدل سازی تفلونی',
        '43': "توری گذار"
    },
    'Q': {
        '10': "اهدا دارو"
    },
    'R': {
        '10': 'کوره آلیاژ سازی  5تن',
        '11': 'کوره آلیاژ سازی  10تن',
        '12': 'کوره ذوب براده',
        '13': 'دستگاه استریر',
        '14': 'دستگاه خشک کن براده',
        '15': 'دستگاه شمش ریزی',
        '16': 'دستگاه مگنت',
    }

}

product_name = {
    '10': 'EC5',
    '11': 'IP20-I',
    '12': 'IP20-II',
    '13': 'K4',
    '14': 'ATV',
    '15': 'کپه یاتاقان 5و1',
    '16': 'ME16',
    '17': 'IK3',
    '18': 'پژو گرویتی',
    '19': 'پیکان',
    '20': 'پراید',
    '21': 'نیسان',
    '23': 'پژو LPDC',
    '24': 'EF7',
    '25': 'TU5',
    '26': 'پژوپارتنر',
    '27': 'کاماز',
    '28': 'M15',
    '29': 'فیات تمپرا',
    '30': 'مسترسیلندر سمند',
    '31': 'مسترسیلندر 206',
    '32': 'ME15',
    '33': 'کپه یاتاقان 3و3',
    '38': 'S81',
    '42': 'کپه یاتاقان 2و4',
    '44': 'E4',
    '55': 'کپه یاتاقان 5و5',
    '57': 'TU3',
    '90': 'عمومی',
    '91': 'ربات',
    '92': 'قطعه گیر',
    '98': 'کوره',
    '99': 'متفرقه',
}

map_source = {
    'N': 'داخلی',
    'X': 'خارجی',
}

map_type = {
    'P': 'پروژه',
    'S': 'یدکی اصلاحی',
    'R': 'تحقیقاتی',
}


def validate_code(code):
    # Extract components from the code
    equipment, subset, product, map_src, map_tp, number = code[:1], code[1:3], code[3:5], code[5], code[6], code[7:]

    if len(code) != 9:
        return False
    # Check if each component is valid
    elif equipment not in equipment_name:
        return False
    elif subset not in equipment_name_subset.get(equipment, {}):
        return False
    elif product not in product_name:
        return False
    elif map_src not in map_source:
        return False
    elif map_tp not in map_type:
        return False
    elif not number.isdigit() or not 1 <= int(number) <= 99:
        return False

    return True


def decode_code(code):
    code = code.upper()
    equipment, subset, product, map_src, map_tp, number = code[:1], code[1:3], code[3:5], code[5], code[6], code[7:]
    # Provide a default message if the key is not found
    equipment_name_str = equipment_name.get(equipment)
    equipment_subset_str = equipment_name_subset.get(equipment, {}).get(subset)
    product_name_str = product_name.get(product)
    if code == "000000000":
        return "امور جاری"
    else:
        return (equipment_name_str + " " +
                equipment_subset_str + " " +
                product_name_str + " " +
                "دست " + number
                )


def decode_code2(code):
    code = code.upper()
    equipment, subset, product, map_src, map_tp, number = code[:1], code[1:3], code[3:5], code[5], code[6], code[7:]

    # Provide a default message if the key is not found
    equipment_name_str = equipment_name.get(equipment, "Unknown Equipment")
    equipment_subset_str = equipment_name_subset.get(equipment, {}).get(subset, "Unknown Subset")
    product_name_str = product_name.get(product, "Unknown Product")
    map_source_str = map_source.get(map_src, "Unknown Source")
    map_tp_str = map_type.get(map_tp, "Unknown Type")

    if code == "000000000":
        return "امور جاری", "امور جاری", "امور جاری"
    else:
        decoded_string = (equipment_name_str + " " +
                          equipment_subset_str + " " +
                          product_name_str + " " +
                          map_source_str + " " +
                          map_tp_str + " " +
                          "دست " + number
                          )
        return decoded_string, map_source_str, map_tp_str
