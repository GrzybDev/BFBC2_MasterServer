from functools import lru_cache

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale

COUNTRY_LIST = {
    "AF": {
        "localizedNames": {
            ClientLocale.English: "Afghanistan",
            ClientLocale.German: "Afghanistan",
            ClientLocale.Spanish: "Afganistán",
            ClientLocale.French: "Afghanistan",
            ClientLocale.Italian: "Afghanistan",
            ClientLocale.Japanese: "アフガニスタン",
            ClientLocale.Polish: "Afganistan",
            ClientLocale.Russian: "Афганистан",
        }
    },
    "AL": {
        "localizedNames": {
            ClientLocale.English: "Albania",
            ClientLocale.German: "Albanien",
            ClientLocale.Spanish: "Albania",
            ClientLocale.French: "Albanie",
            ClientLocale.Italian: "Albania",
            ClientLocale.Japanese: "アルバニア",
            ClientLocale.Polish: "Albania",
            ClientLocale.Russian: "Албания",
        }
    },
    "DZ": {
        "localizedNames": {
            ClientLocale.English: "Algeria",
            ClientLocale.German: "Algerien",
            ClientLocale.Spanish: "Argelia",
            ClientLocale.French: "Algérie",
            ClientLocale.Italian: "Algeria",
            ClientLocale.Japanese: "アルジェリア",
            ClientLocale.Polish: "Algieria",
            ClientLocale.Russian: "Алжир",
        }
    },
    "AS": {
        "localizedNames": {
            ClientLocale.English: "American Samoa",
            ClientLocale.German: "Amerikanisch-Samoa",
            ClientLocale.Spanish: "Samoa Americana",
            ClientLocale.French: "Samoa américaines",
            ClientLocale.Italian: "Samoa americane",
            ClientLocale.Japanese: "米領サモア",
            ClientLocale.Polish: "Amerykańskie Samoa",
            ClientLocale.Russian: "Американское Самоа",
        }
    },
    "AD": {
        "localizedNames": {
            ClientLocale.English: "Andorra",
            ClientLocale.German: "Andorra",
            ClientLocale.Spanish: "Andorra",
            ClientLocale.French: "Andorre",
            ClientLocale.Italian: "Andorra",
            ClientLocale.Japanese: "アンドラ",
            ClientLocale.Polish: "Andora",
            ClientLocale.Russian: "Андорра",
        }
    },
    "AO": {
        "localizedNames": {
            ClientLocale.English: "Angola",
            ClientLocale.German: "Angola",
            ClientLocale.Spanish: "Angola",
            ClientLocale.French: "Angola",
            ClientLocale.Italian: "Angola",
            ClientLocale.Japanese: "アンゴラ",
            ClientLocale.Polish: "Angola",
            ClientLocale.Russian: "Ангола",
        }
    },
    "AI": {
        "localizedNames": {
            ClientLocale.English: "Anguilla",
            ClientLocale.German: "Anguilla",
            ClientLocale.Spanish: "Anguilla",
            ClientLocale.French: "Anguilla",
            ClientLocale.Italian: "Anguilla",
            ClientLocale.Japanese: "アンギラ",
            ClientLocale.Polish: "Anguilla",
            ClientLocale.Russian: "о. Ангилья",
        }
    },
    "AQ": {
        "localizedNames": {
            ClientLocale.English: "Antarctica",
            ClientLocale.German: "Antarktis",
            ClientLocale.Spanish: "Antártida",
            ClientLocale.French: "Antarctique",
            ClientLocale.Italian: "Antartide",
            ClientLocale.Japanese: "南極",
            ClientLocale.Polish: "Antarktyda",
            ClientLocale.Russian: "Антарктида",
        }
    },
    "AG": {
        "localizedNames": {
            ClientLocale.English: "Antigua and Barbuda",
            ClientLocale.German: "Antigua und Barbuda",
            ClientLocale.Spanish: "Antigua y Barbuda",
            ClientLocale.French: "Antigua et Barbuda",
            ClientLocale.Italian: "Antigua e Barbuda",
            ClientLocale.Japanese: "アンティグア・バーブーダ",
            ClientLocale.Polish: "Antigua i Barbuda",
            ClientLocale.Russian: "Антигуа и Барбуда",
        }
    },
    "AR": {
        "localizedNames": {
            ClientLocale.English: "Argentina",
            ClientLocale.German: "Argentinien",
            ClientLocale.Spanish: "Argentina",
            ClientLocale.French: "Argentine",
            ClientLocale.Italian: "Argentina",
            ClientLocale.Japanese: "アルゼンチン",
            ClientLocale.Polish: "Argentyna",
            ClientLocale.Russian: "Аргентина",
        }
    },
    "AM": {
        "localizedNames": {
            ClientLocale.English: "Armenia",
            ClientLocale.German: "Armenien",
            ClientLocale.Spanish: "Armenia",
            ClientLocale.French: "Arménie",
            ClientLocale.Italian: "Armenia",
            ClientLocale.Japanese: "アルメニア",
            ClientLocale.Polish: "Armenia",
            ClientLocale.Russian: "Армения",
        }
    },
    "AW": {
        "localizedNames": {
            ClientLocale.English: "Aruba",
            ClientLocale.German: "Aruba",
            ClientLocale.Spanish: "Aruba",
            ClientLocale.French: "Aruba",
            ClientLocale.Italian: "Aruba",
            ClientLocale.Japanese: "アルバ",
            ClientLocale.Polish: "Aruba",
            ClientLocale.Russian: "Аруба",
        }
    },
    "AU": {
        "localizedNames": {
            ClientLocale.English: "Australia",
            ClientLocale.German: "Australien",
            ClientLocale.Spanish: "Australia",
            ClientLocale.French: "Australie",
            ClientLocale.Italian: "Australia",
            ClientLocale.Japanese: "オーストラリア",
            ClientLocale.Polish: "Australia",
            ClientLocale.Russian: "Австралия",
        }
    },
    "AT": {
        "localizedNames": {
            ClientLocale.English: "Austria",
            ClientLocale.German: "Österreich",
            ClientLocale.Spanish: "Austria",
            ClientLocale.French: "Autriche",
            ClientLocale.Italian: "Austria",
            ClientLocale.Japanese: "オーストリア",
            ClientLocale.Polish: "Austria",
            ClientLocale.Russian: "Австрия",
        }
    },
    "AZ": {
        "localizedNames": {
            ClientLocale.English: "Azerbaijan",
            ClientLocale.German: "Aserbaidschan",
            ClientLocale.Spanish: "Azerbaiyán",
            ClientLocale.French: "Azerbaïdjan",
            ClientLocale.Italian: "Azerbaigian",
            ClientLocale.Japanese: "アゼルバイジャン",
            ClientLocale.Polish: "Azerbejdżan",
            ClientLocale.Russian: "Азербайджан",
        }
    },
    "BS": {
        "localizedNames": {
            ClientLocale.English: "Bahamas",
            ClientLocale.German: "Bahamas",
            ClientLocale.Spanish: "Bahamas",
            ClientLocale.French: "Bahamas",
            ClientLocale.Italian: "Bahama",
            ClientLocale.Japanese: "バハマ",
            ClientLocale.Polish: "Wyspy Bahama",
            ClientLocale.Russian: "Багамские о-ва",
        }
    },
    "BH": {
        "localizedNames": {
            ClientLocale.English: "Bahrain",
            ClientLocale.German: "Bahrain",
            ClientLocale.Spanish: "Bahrein",
            ClientLocale.French: "Bahreïn",
            ClientLocale.Italian: "Bahrein",
            ClientLocale.Japanese: "バーレーン",
            ClientLocale.Polish: "Bahrain",
            ClientLocale.Russian: "Бахрейн",
        }
    },
    "BD": {
        "localizedNames": {
            ClientLocale.English: "Bangladesh",
            ClientLocale.German: "Bangladesch",
            ClientLocale.Spanish: "Bangladesh",
            ClientLocale.French: "Bangladesh",
            ClientLocale.Italian: "Bangladesh",
            ClientLocale.Japanese: "バングラデシュ",
            ClientLocale.Polish: "Bangladesz",
            ClientLocale.Russian: "Бангладеш",
        }
    },
    "BB": {
        "localizedNames": {
            ClientLocale.English: "Barbados",
            ClientLocale.German: "Barbados",
            ClientLocale.Spanish: "Barbados",
            ClientLocale.French: "Barbade",
            ClientLocale.Italian: "Barbados",
            ClientLocale.Japanese: "バルバドス",
            ClientLocale.Polish: "Barbados",
            ClientLocale.Russian: "Барбадос",
        }
    },
    "BY": {
        "localizedNames": {
            ClientLocale.English: "Belarus",
            ClientLocale.German: "Weißrussland",
            ClientLocale.Spanish: "Bielorrusia",
            ClientLocale.French: "Biélorussie",
            ClientLocale.Italian: "Bielorussia",
            ClientLocale.Japanese: "ベラルーシ",
            ClientLocale.Polish: "Białoruś",
            ClientLocale.Russian: "Беларусь",
        }
    },
    "BE": {
        "localizedNames": {
            ClientLocale.English: "Belgium",
            ClientLocale.German: "Belgien",
            ClientLocale.Spanish: "Bélgica",
            ClientLocale.French: "Belgique",
            ClientLocale.Italian: "Belgio",
            ClientLocale.Japanese: "ベルギー",
            ClientLocale.Polish: "Belgia",
            ClientLocale.Russian: "Бельгия",
        }
    },
    "BZ": {
        "localizedNames": {
            ClientLocale.English: "Belize",
            ClientLocale.German: "Belize",
            ClientLocale.Spanish: "Belize",
            ClientLocale.French: "Belize",
            ClientLocale.Italian: "Belize",
            ClientLocale.Japanese: "ベリーズ",
            ClientLocale.Polish: "Belize",
            ClientLocale.Russian: "Белиз",
        }
    },
    "BJ": {
        "localizedNames": {
            ClientLocale.English: "Benin",
            ClientLocale.German: "Benin",
            ClientLocale.Spanish: "Benin",
            ClientLocale.French: "Bénin",
            ClientLocale.Italian: "Benin",
            ClientLocale.Japanese: "ベナン",
            ClientLocale.Polish: "Benin",
            ClientLocale.Russian: "Бенин",
        }
    },
    "BM": {
        "localizedNames": {
            ClientLocale.English: "Bermuda",
            ClientLocale.German: "Bermuda",
            ClientLocale.Spanish: "Las Bermudas",
            ClientLocale.French: "Bermudes",
            ClientLocale.Italian: "Bermuda",
            ClientLocale.Japanese: "バミューダ諸島",
            ClientLocale.Polish: "Bermudy",
            ClientLocale.Russian: "Бермудские о-ва",
        }
    },
    "BT": {
        "localizedNames": {
            ClientLocale.English: "Bhutan",
            ClientLocale.German: "Bhutan",
            ClientLocale.Spanish: "Bhutan",
            ClientLocale.French: "Bhoutan",
            ClientLocale.Italian: "Bhutan",
            ClientLocale.Japanese: "ブータン",
            ClientLocale.Polish: "Butan",
            ClientLocale.Russian: "Бутан",
        }
    },
    "BO": {
        "localizedNames": {
            ClientLocale.English: "Bolivia",
            ClientLocale.German: "Bolivien",
            ClientLocale.Spanish: "Bolivia",
            ClientLocale.French: "Bolivie",
            ClientLocale.Italian: "Bolivia",
            ClientLocale.Japanese: "ボリビア",
            ClientLocale.Polish: "Boliwia",
            ClientLocale.Russian: "Боливия",
        }
    },
    "BA": {
        "localizedNames": {
            ClientLocale.English: "Bosnia and Herzegovina",
            ClientLocale.German: "Bosnien und Herzegowina",
            ClientLocale.Spanish: "Bosnia y Herzegovina",
            ClientLocale.French: "Bosnie-Herzégovine",
            ClientLocale.Italian: "Bosnia-Erzegovina",
            ClientLocale.Japanese: "ボスニア・ヘルツェゴビナ",
            ClientLocale.Polish: "Bośnia i Hercegowina",
            ClientLocale.Russian: "Босния и Герцеговина",
        }
    },
    "BW": {
        "localizedNames": {
            ClientLocale.English: "Botswana",
            ClientLocale.German: "Botswana",
            ClientLocale.Spanish: "Botswana",
            ClientLocale.French: "Botswana",
            ClientLocale.Italian: "Botswana",
            ClientLocale.Japanese: "ボツワナ",
            ClientLocale.Polish: "Botswana",
            ClientLocale.Russian: "Ботсвана",
        }
    },
    "BV": {
        "localizedNames": {
            ClientLocale.English: "Bouvet Island",
            ClientLocale.German: "Bouvet-Insel",
            ClientLocale.Spanish: "Isla Bouvet",
            ClientLocale.French: "Iles Bouvet",
            ClientLocale.Italian: "Isola Bouvet",
            ClientLocale.Japanese: "ブーベ島",
            ClientLocale.Polish: "Wyspa Bouvet",
            ClientLocale.Russian: "О. Буве",
        }
    },
    "BR": {
        "localizedNames": {
            ClientLocale.English: "Brazil",
            ClientLocale.German: "Brasilien",
            ClientLocale.Spanish: "Brasil",
            ClientLocale.French: "Brésil",
            ClientLocale.Italian: "Brasile",
            ClientLocale.Japanese: "ブラジル",
            ClientLocale.Polish: "Brazylia",
            ClientLocale.Russian: "Бразилия",
        }
    },
    "IO": {
        "localizedNames": {
            ClientLocale.English: "British Indian Ocean Territory",
            ClientLocale.German: "Britisches Territorium im Indischen Ozean",
            ClientLocale.Spanish: "Territorio oceánico de la India británica",
            ClientLocale.French: "Territoires britanniques de l'océan Indien",
            ClientLocale.Italian: "Territorio inglese nell’Oceano Indiano",
            ClientLocale.Japanese: "英領インド洋地域",
            ClientLocale.Polish: "Brytyjskie Terytorium na Oceanie Indyjskim",
            ClientLocale.Russian: "Брит. терр. в Инд. океане",
        }
    },
    "VG": {
        "localizedNames": {
            ClientLocale.English: "British Virgin Islands",
            ClientLocale.German: "Jungfraueninseln (GB)",
            ClientLocale.Spanish: "Islas Vírgenes británicas",
            ClientLocale.French: "Iles Vierges du Royaume-Uni",
            ClientLocale.Italian: "Isole Vergini Britanniche",
            ClientLocale.Japanese: "英領バージン諸島",
            ClientLocale.Polish: "Wyspy Dziewicze Brytyjskie",
            ClientLocale.Russian: "Британские Виргинские О-ва",
        }
    },
    "BN": {
        "localizedNames": {
            ClientLocale.English: "Brunei",
            ClientLocale.German: "Brunei",
            ClientLocale.Spanish: "Brunei",
            ClientLocale.French: "Brunei",
            ClientLocale.Italian: "Brunei",
            ClientLocale.Japanese: "ブルネイ",
            ClientLocale.Polish: "Brunei",
            ClientLocale.Russian: "Бруней",
        }
    },
    "BG": {
        "localizedNames": {
            ClientLocale.English: "Bulgaria",
            ClientLocale.German: "Bulgarien",
            ClientLocale.Spanish: "Bulgaria",
            ClientLocale.French: "Bulgarie",
            ClientLocale.Italian: "Bulgaria",
            ClientLocale.Japanese: "ブルガリア",
            ClientLocale.Polish: "Bułgaria",
            ClientLocale.Russian: "Болгария",
        }
    },
    "BF": {
        "localizedNames": {
            ClientLocale.English: "Burkina Faso",
            ClientLocale.German: "Burkina Faso",
            ClientLocale.Spanish: "Burkina Faso",
            ClientLocale.French: "Burkina Faso",
            ClientLocale.Italian: "Burkina Faso",
            ClientLocale.Japanese: "ブルキナファソ",
            ClientLocale.Polish: "Burkina Faso",
            ClientLocale.Russian: "Буркина-Фасо",
        }
    },
    "BI": {
        "localizedNames": {
            ClientLocale.English: "Burundi",
            ClientLocale.German: "Burundi",
            ClientLocale.Spanish: "Burundi",
            ClientLocale.French: "Burundi",
            ClientLocale.Italian: "Burundi",
            ClientLocale.Japanese: "ブルンジ",
            ClientLocale.Polish: "Burundi",
            ClientLocale.Russian: "Бурунди",
        }
    },
    "KH": {
        "localizedNames": {
            ClientLocale.English: "Cambodia",
            ClientLocale.German: "Kambodscha",
            ClientLocale.Spanish: "Camboya",
            ClientLocale.French: "Cambodge",
            ClientLocale.Italian: "Cambogia",
            ClientLocale.Japanese: "カンボジア",
            ClientLocale.Polish: "Kambodża",
            ClientLocale.Russian: "Камбоджа",
        }
    },
    "CM": {
        "localizedNames": {
            ClientLocale.English: "Cameroon",
            ClientLocale.German: "Kamerun",
            ClientLocale.Spanish: "Camerún",
            ClientLocale.French: "Cameroun",
            ClientLocale.Italian: "Camerun",
            ClientLocale.Japanese: "カメルーン",
            ClientLocale.Polish: "Kamerun",
            ClientLocale.Russian: "Камерун",
        }
    },
    "CA": {
        "localizedNames": {
            ClientLocale.English: "Canada",
            ClientLocale.German: "Kanada",
            ClientLocale.Spanish: "Canadá",
            ClientLocale.French: "Canada",
            ClientLocale.Italian: "Canada",
            ClientLocale.Japanese: "カナダ",
            ClientLocale.Polish: "Kanada",
            ClientLocale.Russian: "Канада",
        },
        "allowEmailsDefaultValue": True,
    },
    "CV": {
        "localizedNames": {
            ClientLocale.English: "Cape Verde",
            ClientLocale.German: "Kap Verde",
            ClientLocale.Spanish: "Cabo Verde",
            ClientLocale.French: "Cap Vert",
            ClientLocale.Italian: "Capo Verde",
            ClientLocale.Japanese: "カボベルデ",
            ClientLocale.Polish: "Cape Verde",
            ClientLocale.Russian: "Кабо-Верде",
        }
    },
    "KY": {
        "localizedNames": {
            ClientLocale.English: "Cayman Islands",
            ClientLocale.German: "Kaimaninseln",
            ClientLocale.Spanish: "Islas Caimán",
            ClientLocale.French: "Iles Caïmans",
            ClientLocale.Italian: "Isole Cayman",
            ClientLocale.Japanese: "ケイマン諸島",
            ClientLocale.Polish: "Kajmany",
            ClientLocale.Russian: "Каймановы о-ва",
        }
    },
    "CF": {
        "localizedNames": {
            ClientLocale.English: "Central African Republic",
            ClientLocale.German: "Zentralafrikanische Republik",
            ClientLocale.Spanish: "República Centroafricana",
            ClientLocale.French: "République centrafricaine",
            ClientLocale.Italian: "Repubblica Centrafricana",
            ClientLocale.Japanese: "中央アフリカ",
            ClientLocale.Polish: "Republika Środkowej Afryki",
            ClientLocale.Russian: "Центральноафриканская Республика",
        }
    },
    "TD": {
        "localizedNames": {
            ClientLocale.English: "Chad",
            ClientLocale.German: "Tschad",
            ClientLocale.Spanish: "Chad",
            ClientLocale.French: "Tchad",
            ClientLocale.Italian: "Ciad",
            ClientLocale.Japanese: "チャド",
            ClientLocale.Polish: "Czad",
            ClientLocale.Russian: "Чад",
        }
    },
    "CL": {
        "localizedNames": {
            ClientLocale.English: "Chile",
            ClientLocale.German: "Chile",
            ClientLocale.Spanish: "Chile",
            ClientLocale.French: "Chili",
            ClientLocale.Italian: "Cile",
            ClientLocale.Japanese: "チリ",
            ClientLocale.Polish: "Chile",
            ClientLocale.Russian: "Чили",
        }
    },
    "CN": {
        "localizedNames": {
            ClientLocale.English: "China",
            ClientLocale.German: "China",
            ClientLocale.Spanish: "China",
            ClientLocale.French: "Chine",
            ClientLocale.Italian: "Cina",
            ClientLocale.Japanese: "中国",
            ClientLocale.Polish: "Chiny",
            ClientLocale.Russian: "Китай",
        }
    },
    "CX": {
        "localizedNames": {
            ClientLocale.English: "Christmas Island",
            ClientLocale.German: "Weihnachtsinsel",
            ClientLocale.Spanish: "Islas Christmas",
            ClientLocale.French: "Ile Christmas",
            ClientLocale.Italian: "Isola Christmas",
            ClientLocale.Japanese: "ク リスマス島",
            ClientLocale.Polish: "Wyspa Bożego Narodzenia",
            ClientLocale.Russian: "О. Рождества",
        }
    },
    "CC": {
        "localizedNames": {
            ClientLocale.English: "Cocos Islands",
            ClientLocale.German: "Cocos-Inseln",
            ClientLocale.Spanish: "Islas Cocos",
            ClientLocale.French: "Iles Cocos",
            ClientLocale.Italian: "Isole Cocos",
            ClientLocale.Japanese: "ココス諸島",
            ClientLocale.Polish: "Wyspy Kokosowe",
            ClientLocale.Russian: "Кокосовые о-ва",
        }
    },
    "CO": {
        "localizedNames": {
            ClientLocale.English: "Colombia",
            ClientLocale.German: "Kolumbien",
            ClientLocale.Spanish: "Colombia",
            ClientLocale.French: "Colombie",
            ClientLocale.Italian: "Colombia",
            ClientLocale.Japanese: "コロンビア",
            ClientLocale.Polish: "Kolumbia",
            ClientLocale.Russian: "Колумбия",
        }
    },
    "KM": {
        "localizedNames": {
            ClientLocale.English: "Comoros",
            ClientLocale.German: "Komoren",
            ClientLocale.Spanish: "Comores",
            ClientLocale.French: "Comores",
            ClientLocale.Italian: "Isole Comore",
            ClientLocale.Japanese: "コモロ",
            ClientLocale.Polish: "Komory",
            ClientLocale.Russian: "Коморские о-ва",
        }
    },
    "CD": {
        "localizedNames": {
            ClientLocale.English: "Congo, Democratic Republic of",
            ClientLocale.German: "Demokratische Republik Kongo",
            ClientLocale.Spanish: "República Democrática del Congo",
            ClientLocale.French: "Congo, République démocratique du ",
            ClientLocale.Italian: "Congo, Repubblica Democratica del",
            ClientLocale.Japanese: "コンゴ民主共和国",
            ClientLocale.Polish: "Demokratyczna Republika Konga",
            ClientLocale.Russian: "Демократическая Республика Конго",
        }
    },
    "CG": {
        "localizedNames": {
            ClientLocale.English: "Congo, People's Republic of",
            ClientLocale.German: "Volksrepublik Kongo",
            ClientLocale.Spanish: "República Popular del Congo",
            ClientLocale.French: "Congo, République populaire du ",
            ClientLocale.Italian: "Congo, Repubblica Popolare del",
            ClientLocale.Japanese: "コンゴ共和国",
            ClientLocale.Polish: "Ludowa Republika Konga",
            ClientLocale.Russian: "Народная Республика Конго",
        }
    },
    "CK": {
        "localizedNames": {
            ClientLocale.English: "Cook Islands",
            ClientLocale.German: "Cook-Inseln",
            ClientLocale.Spanish: "Islas Cook",
            ClientLocale.French: "Iles Cook",
            ClientLocale.Italian: "Isole Cook",
            ClientLocale.Japanese: "クック諸島",
            ClientLocale.Polish: "Wyspy Cooka",
            ClientLocale.Russian: "О-ва Кука",
        }
    },
    "CR": {
        "localizedNames": {
            ClientLocale.English: "Costa Rica",
            ClientLocale.German: "Costa Rica",
            ClientLocale.Spanish: "Costa Rica",
            ClientLocale.French: "Costa Rica",
            ClientLocale.Italian: "Costa Rica",
            ClientLocale.Japanese: "コスタリカ",
            ClientLocale.Polish: "Costa Rica",
            ClientLocale.Russian: "Коста-Рика",
        }
    },
    "HR": {
        "localizedNames": {
            ClientLocale.English: "Croatia",
            ClientLocale.German: "Kroatien",
            ClientLocale.Spanish: "Croacia",
            ClientLocale.French: "Croatie",
            ClientLocale.Italian: "Croazia",
            ClientLocale.Japanese: "クロアチア",
            ClientLocale.Polish: "Chorwacja",
            ClientLocale.Russian: "Хорватия",
        }
    },
    "CY": {
        "localizedNames": {
            ClientLocale.English: "Cyprus",
            ClientLocale.German: "Zypern",
            ClientLocale.Spanish: "Chipre",
            ClientLocale.French: "Chypre",
            ClientLocale.Italian: "Cipro",
            ClientLocale.Japanese: "キプロス",
            ClientLocale.Polish: "Cypr",
            ClientLocale.Russian: "Кипр",
        }
    },
    "CZ": {
        "localizedNames": {
            ClientLocale.English: "Czech Republic",
            ClientLocale.German: "Tschechische Republik",
            ClientLocale.Spanish: "República Checa",
            ClientLocale.French: "République tchèque",
            ClientLocale.Italian: "Repubblica Ceca",
            ClientLocale.Japanese: "チェコ",
            ClientLocale.Polish: "Czechy",
            ClientLocale.Russian: "Чехия",
        }
    },
    "DK": {
        "localizedNames": {
            ClientLocale.English: "Denmark",
            ClientLocale.German: "Dänemark",
            ClientLocale.Spanish: "Dinamarca",
            ClientLocale.French: "Danemark",
            ClientLocale.Italian: "Danimarca",
            ClientLocale.Japanese: "デンマーク",
            ClientLocale.Polish: "Dania",
            ClientLocale.Russian: "Дания",
        }
    },
    "DJ": {
        "localizedNames": {
            ClientLocale.English: "Djibouti",
            ClientLocale.German: "Dschibuti",
            ClientLocale.Spanish: "Yibuti",
            ClientLocale.French: "Djibouti",
            ClientLocale.Italian: "Gibuti",
            ClientLocale.Japanese: "ジブチ",
            ClientLocale.Polish: "Dżibuti",
            ClientLocale.Russian: "Джибути",
        }
    },
    "DM": {
        "localizedNames": {
            ClientLocale.English: "Dominica",
            ClientLocale.German: "Dominica",
            ClientLocale.Spanish: "Dominica",
            ClientLocale.French: "Dominique",
            ClientLocale.Italian: "Dominica",
            ClientLocale.Japanese: "ドミニカ",
            ClientLocale.Polish: "Dominika",
            ClientLocale.Russian: "Доминика",
        }
    },
    "DO": {
        "localizedNames": {
            ClientLocale.English: "Dominican Republic",
            ClientLocale.German: "Dominikanische Republik",
            ClientLocale.Spanish: "República Dominicana",
            ClientLocale.French: "République dominicaine",
            ClientLocale.Italian: "Repubblica Dominicana",
            ClientLocale.Japanese: "ドミニカ共和国",
            ClientLocale.Polish: "Republika Dominikańska",
            ClientLocale.Russian: "Доминиканская Республика",
        }
    },
    "TL": {
        "localizedNames": {
            ClientLocale.English: "East Timor",
            ClientLocale.German: "Osttimor",
            ClientLocale.Spanish: "Timor Oriental",
            ClientLocale.French: "Timor oriental",
            ClientLocale.Italian: "Timor Est",
            ClientLocale.Japanese: "東ティモール",
            ClientLocale.Polish: "Timor Wschodni",
            ClientLocale.Russian: "Восточный Тимор",
        }
    },
    "EC": {
        "localizedNames": {
            ClientLocale.English: "Ecuador",
            ClientLocale.German: "Ecuador",
            ClientLocale.Spanish: "Ecuador",
            ClientLocale.French: "Equateur",
            ClientLocale.Italian: "Ecuador",
            ClientLocale.Japanese: "エクアドル",
            ClientLocale.Polish: "Ekwador",
            ClientLocale.Russian: "Эквадор",
        }
    },
    "EG": {
        "localizedNames": {
            ClientLocale.English: "Egypt",
            ClientLocale.German: "Ägypten",
            ClientLocale.Spanish: "Egipto",
            ClientLocale.French: "Egypte",
            ClientLocale.Italian: "Egitto",
            ClientLocale.Japanese: "エジプト",
            ClientLocale.Polish: "Egipt",
            ClientLocale.Russian: "Египет",
        }
    },
    "SV": {
        "localizedNames": {
            ClientLocale.English: "El Salvador",
            ClientLocale.German: "El Salvador",
            ClientLocale.Spanish: "El Salvador",
            ClientLocale.French: "Salvador",
            ClientLocale.Italian: "El Salvador",
            ClientLocale.Japanese: "エルサルバドル",
            ClientLocale.Polish: "El Salvador",
            ClientLocale.Russian: "Сальвадор",
        }
    },
    "GQ": {
        "localizedNames": {
            ClientLocale.English: "Equatorial Guinea",
            ClientLocale.German: "Äquatorialguinea",
            ClientLocale.Spanish: "Guinea Ecuatorial",
            ClientLocale.French: "Guinée équatoriale",
            ClientLocale.Italian: "Guinea Equatoriale",
            ClientLocale.Japanese: "赤道ギニア",
            ClientLocale.Polish: "Gwinea Równikowa",
            ClientLocale.Russian: "Экваториальная Гвинея",
        }
    },
    "ER": {
        "localizedNames": {
            ClientLocale.English: "Eritrea",
            ClientLocale.German: "Eritrea",
            ClientLocale.Spanish: "Eritrea",
            ClientLocale.French: "Erythrée",
            ClientLocale.Italian: "Eritrea",
            ClientLocale.Japanese: "エリトリア",
            ClientLocale.Polish: "Erytrea",
            ClientLocale.Russian: "Эритрея",
        }
    },
    "EE": {
        "localizedNames": {
            ClientLocale.English: "Estonia",
            ClientLocale.German: "Estland",
            ClientLocale.Spanish: "Estonia",
            ClientLocale.French: "Estonie",
            ClientLocale.Italian: "Estonia",
            ClientLocale.Japanese: "エストニア",
            ClientLocale.Polish: "Estonia",
            ClientLocale.Russian: "Эстония",
        }
    },
    "ET": {
        "localizedNames": {
            ClientLocale.English: "Ethiopia",
            ClientLocale.German: "Äthiopien",
            ClientLocale.Spanish: "Etiopía",
            ClientLocale.French: "Ethiopie",
            ClientLocale.Italian: "Etiopia",
            ClientLocale.Japanese: "エチオピア",
            ClientLocale.Polish: "Etiopia",
            ClientLocale.Russian: "Эфиопия",
        }
    },
    "FO": {
        "localizedNames": {
            ClientLocale.English: "Faeroe Islands",
            ClientLocale.German: "Färöerinseln",
            ClientLocale.Spanish: "Islas Feroe",
            ClientLocale.French: "Iles Féroé",
            ClientLocale.Italian: "Isole Faroe",
            ClientLocale.Japanese: "フェロー諸島",
            ClientLocale.Polish: "Wyspy Owcze",
            ClientLocale.Russian: "Фарерские о-ва",
        }
    },
    "FK": {
        "localizedNames": {
            ClientLocale.English: "Falkland Islands (Malvinas)",
            ClientLocale.German: "Falklandinseln (Malvinen)",
            ClientLocale.Spanish: "Islas Falkland (Malvinas)",
            ClientLocale.French: "Iles Falkland (Malouines)",
            ClientLocale.Italian: "Isole Falkland",
            ClientLocale.Japanese: "フォークランド諸島",
            ClientLocale.Polish: "Falklandy",
            ClientLocale.Russian: "Фолклендские (Мальвинские) о-ва",
        }
    },
    "FJ": {
        "localizedNames": {
            ClientLocale.English: "Fiji",
            ClientLocale.German: "Fidschiinseln",
            ClientLocale.Spanish: "Fiyi",
            ClientLocale.French: "Fidji",
            ClientLocale.Italian: "Figi",
            ClientLocale.Japanese: "フィジー",
            ClientLocale.Polish: "Fidżi",
            ClientLocale.Russian: "О-ва Фиджи",
        }
    },
    "FI": {
        "localizedNames": {
            ClientLocale.English: "Finland",
            ClientLocale.German: "Finnland",
            ClientLocale.Spanish: "Finlandia",
            ClientLocale.French: "Finlande",
            ClientLocale.Italian: "Finlandia",
            ClientLocale.Japanese: "フィンランド",
            ClientLocale.Polish: "Finlandia",
            ClientLocale.Russian: "Финляндия",
        }
    },
    "FR": {
        "localizedNames": {
            ClientLocale.English: "France",
            ClientLocale.German: "Frankreich",
            ClientLocale.Spanish: "Francia",
            ClientLocale.French: "France",
            ClientLocale.Italian: "Francia",
            ClientLocale.Japanese: "フランス",
            ClientLocale.Polish: "Francja",
            ClientLocale.Russian: "Франция",
        },
        "parentalControlAgeLimit": 16,
        "registrationAgeLimit": 16,
    },
    "GF": {
        "localizedNames": {
            ClientLocale.English: "French Guiana",
            ClientLocale.German: "Französisch-Guayana",
            ClientLocale.Spanish: "Guayana Francesa",
            ClientLocale.French: "Guyane française",
            ClientLocale.Italian: "Guyana Francese",
            ClientLocale.Japanese: "仏領ギアナ",
            ClientLocale.Polish: "Gujana Francuska",
            ClientLocale.Russian: "Французская Гвиана",
        }
    },
    "PF": {
        "localizedNames": {
            ClientLocale.English: "French Polynesia",
            ClientLocale.German: "Französisch-Polynesien",
            ClientLocale.Spanish: "Polinesia Francesa",
            ClientLocale.French: "Polynésie française",
            ClientLocale.Italian: "Polinesia Francese",
            ClientLocale.Japanese: "仏領ポリネシア",
            ClientLocale.Polish: "Polinezja Francuska",
            ClientLocale.Russian: "Французская Полинезия",
        }
    },
    "TF": {
        "localizedNames": {
            ClientLocale.English: "French Southern Territories",
            ClientLocale.German: "Französische Südterritorien",
            ClientLocale.Spanish: "Territorios del Sur de Francia",
            ClientLocale.French: "Terres australes et antarctiques françaises",
            ClientLocale.Italian: "Territori Meridionali Francesi",
            ClientLocale.Japanese: "仏南方領",
            ClientLocale.Polish: "Francuskie Terytorium Południowe",
            ClientLocale.Russian: "Франц. Южн. Терр.",
        }
    },
    "GA": {
        "localizedNames": {
            ClientLocale.English: "Gabon",
            ClientLocale.German: "Gabun",
            ClientLocale.Spanish: "Gabón",
            ClientLocale.French: "Gabon",
            ClientLocale.Italian: "Gabon",
            ClientLocale.Japanese: "ガボン",
            ClientLocale.Polish: "Gabon",
            ClientLocale.Russian: "Габон",
        }
    },
    "GM": {
        "localizedNames": {
            ClientLocale.English: "Gambia",
            ClientLocale.German: "Gambia",
            ClientLocale.Spanish: "Gambia",
            ClientLocale.French: "Gambie",
            ClientLocale.Italian: "Gambia",
            ClientLocale.Japanese: "ガンビア",
            ClientLocale.Polish: "Gambia",
            ClientLocale.Russian: "Гамбия",
        }
    },
    "GE": {
        "localizedNames": {
            ClientLocale.English: "Georgia",
            ClientLocale.German: "Georgien",
            ClientLocale.Spanish: "Georgia",
            ClientLocale.French: "Géorgie",
            ClientLocale.Italian: "Georgia",
            ClientLocale.Japanese: "グルジア",
            ClientLocale.Polish: "Gruzja",
            ClientLocale.Russian: "Грузия",
        }
    },
    "DE": {
        "localizedNames": {
            ClientLocale.English: "Germany",
            ClientLocale.German: "Deutschland",
            ClientLocale.Spanish: "Alemania",
            ClientLocale.French: "Allemagne",
            ClientLocale.Italian: "Germania",
            ClientLocale.Japanese: "ドイツ",
            ClientLocale.Polish: "Niemcy",
            ClientLocale.Russian: "Германия",
        },
        "parentalControlAgeLimit": 14,
        "registrationAgeLimit": 14,
    },
    "GH": {
        "localizedNames": {
            ClientLocale.English: "Ghana",
            ClientLocale.German: "Ghana",
            ClientLocale.Spanish: "Ghana",
            ClientLocale.French: "Ghana",
            ClientLocale.Italian: "Ghana",
            ClientLocale.Japanese: "ガーナ",
            ClientLocale.Polish: "Ghana",
            ClientLocale.Russian: "Гана",
        }
    },
    "GI": {
        "localizedNames": {
            ClientLocale.English: "Gibraltar",
            ClientLocale.German: "Gibraltar",
            ClientLocale.Spanish: "Gibraltar",
            ClientLocale.French: "Gibraltar",
            ClientLocale.Italian: "Gibilterra",
            ClientLocale.Japanese: "ジブラルタル",
            ClientLocale.Polish: "Gibraltar",
            ClientLocale.Russian: "Гибралтар",
        }
    },
    "GR": {
        "localizedNames": {
            ClientLocale.English: "Greece",
            ClientLocale.German: "Griechenland",
            ClientLocale.Spanish: "Grecia",
            ClientLocale.French: "Grèce",
            ClientLocale.Italian: "Grecia",
            ClientLocale.Japanese: "ギリシャ",
            ClientLocale.Polish: "Grecja",
            ClientLocale.Russian: "Греция",
        }
    },
    "GL": {
        "localizedNames": {
            ClientLocale.English: "Greenland",
            ClientLocale.German: "Grönland",
            ClientLocale.Spanish: "Groenlandia",
            ClientLocale.French: "Groenland",
            ClientLocale.Italian: "Groenlandia",
            ClientLocale.Japanese: "グリーンランド",
            ClientLocale.Polish: "Grenlandia",
            ClientLocale.Russian: "Гренландия",
        }
    },
    "GD": {
        "localizedNames": {
            ClientLocale.English: "Grenada",
            ClientLocale.German: "Grenada",
            ClientLocale.Spanish: "Granada",
            ClientLocale.French: "Grenade",
            ClientLocale.Italian: "Grenada",
            ClientLocale.Japanese: "グレナダ",
            ClientLocale.Polish: "Grenada",
            ClientLocale.Russian: "Гренада",
        }
    },
    "GP": {
        "localizedNames": {
            ClientLocale.English: "Guadaloupe",
            ClientLocale.German: "Guadeloupe",
            ClientLocale.Spanish: "Guadalupe",
            ClientLocale.French: "Guadeloupe",
            ClientLocale.Italian: "Guadalupe",
            ClientLocale.Japanese: "グアドループ島",
            ClientLocale.Polish: "Gwadelupa",
            ClientLocale.Russian: "Гваделупа",
        }
    },
    "GU": {
        "localizedNames": {
            ClientLocale.English: "Guam",
            ClientLocale.German: "Guam",
            ClientLocale.Spanish: "Guam",
            ClientLocale.French: "Guam",
            ClientLocale.Italian: "Guam",
            ClientLocale.Japanese: "グアム",
            ClientLocale.Polish: "Guam",
            ClientLocale.Russian: "О. Гуам",
        }
    },
    "GT": {
        "localizedNames": {
            ClientLocale.English: "Guatemala",
            ClientLocale.German: "Guatemala",
            ClientLocale.Spanish: "Guatemala",
            ClientLocale.French: "Guatemala",
            ClientLocale.Italian: "Guatemala",
            ClientLocale.Japanese: "グアテマラ",
            ClientLocale.Polish: "Gwatemala",
            ClientLocale.Russian: "Гватемала",
        }
    },
    "GN": {
        "localizedNames": {
            ClientLocale.English: "Guinea",
            ClientLocale.German: "Guinea",
            ClientLocale.Spanish: "Guinea",
            ClientLocale.French: "Guinée",
            ClientLocale.Italian: "Guinea",
            ClientLocale.Japanese: "ギニア",
            ClientLocale.Polish: "Gwinea",
            ClientLocale.Russian: "Гвинея",
        }
    },
    "GW": {
        "localizedNames": {
            ClientLocale.English: "Guinea-Bissau",
            ClientLocale.German: "Guinea-Bissau",
            ClientLocale.Spanish: "Guinea-Bissau",
            ClientLocale.French: "Guinée-Bissau",
            ClientLocale.Italian: "Guinea-Bissau",
            ClientLocale.Japanese: "ギニアビサウ",
            ClientLocale.Polish: "Gwinea-Bissau",
            ClientLocale.Russian: "Гвинея-Бисау",
        }
    },
    "GY": {
        "localizedNames": {
            ClientLocale.English: "Guyana, Republic of",
            ClientLocale.German: "Republik Guyana",
            ClientLocale.Spanish: "República de Guayana",
            ClientLocale.French: "Guyana, République coopérative de ",
            ClientLocale.Italian: "Guyana, Repubblica della",
            ClientLocale.Japanese: "ガイアナ",
            ClientLocale.Polish: "Republika Gujany",
            ClientLocale.Russian: "Республика Гайана",
        }
    },
    "HT": {
        "localizedNames": {
            ClientLocale.English: "Haiti",
            ClientLocale.German: "Haiti",
            ClientLocale.Spanish: "Haití",
            ClientLocale.French: "Haïti",
            ClientLocale.Italian: "Haiti",
            ClientLocale.Japanese: "ハイチ",
            ClientLocale.Polish: "Haiti",
            ClientLocale.Russian: "Гаити",
        }
    },
    "HM": {
        "localizedNames": {
            ClientLocale.English: "Heard and McDonald Islands",
            ClientLocale.German: "Heard- und McDonald-Inseln",
            ClientLocale.Spanish: "Islas Heard y McDonald",
            ClientLocale.French: "Iles Heard et McDonald",
            ClientLocale.Italian: "Isole Heard e McDonald",
            ClientLocale.Japanese: "ハード・マクドナルド諸島",
            ClientLocale.Polish: "Wyspy Heard i McDonalda",
            ClientLocale.Russian: "О-ва\xa0Херд\xa0и\xa0Макдональд",
        }
    },
    "HN": {
        "localizedNames": {
            ClientLocale.English: "Honduras",
            ClientLocale.German: "Honduras",
            ClientLocale.Spanish: "Honduras",
            ClientLocale.French: "Honduras",
            ClientLocale.Italian: "Honduras",
            ClientLocale.Japanese: "ホンジュラス",
            ClientLocale.Polish: "Honduras",
            ClientLocale.Russian: "Гондурас",
        }
    },
    "HU": {
        "localizedNames": {
            ClientLocale.English: "Hungary",
            ClientLocale.German: "Ungarn",
            ClientLocale.Spanish: "Hungría",
            ClientLocale.French: "Hongrie",
            ClientLocale.Italian: "Ungheria",
            ClientLocale.Japanese: "ハンガリー",
            ClientLocale.Polish: "Węgry",
            ClientLocale.Russian: "Венгрия",
        }
    },
    "IS": {
        "localizedNames": {
            ClientLocale.English: "Iceland",
            ClientLocale.German: "Island",
            ClientLocale.Spanish: "Islandia",
            ClientLocale.French: "Islande",
            ClientLocale.Italian: "Islanda",
            ClientLocale.Japanese: "アイスランド",
            ClientLocale.Polish: "Islandia",
            ClientLocale.Russian: "Исландия",
        }
    },
    "IN": {
        "localizedNames": {
            ClientLocale.English: "India",
            ClientLocale.German: "Indien",
            ClientLocale.Spanish: "India",
            ClientLocale.French: "Inde",
            ClientLocale.Italian: "India",
            ClientLocale.Japanese: "インド",
            ClientLocale.Polish: "India",
            ClientLocale.Russian: "Индия",
        }
    },
    "ID": {
        "localizedNames": {
            ClientLocale.English: "Indonesia",
            ClientLocale.German: "Indonesien",
            ClientLocale.Spanish: "Indonesia",
            ClientLocale.French: "Indonésie",
            ClientLocale.Italian: "Indonesia",
            ClientLocale.Japanese: "インドネシア",
            ClientLocale.Polish: "Indonezja",
            ClientLocale.Russian: "Индонезия",
        }
    },
    "IE": {
        "localizedNames": {
            ClientLocale.English: "Ireland",
            ClientLocale.German: "Irland",
            ClientLocale.Spanish: "Irlanda",
            ClientLocale.French: "Irlande",
            ClientLocale.Italian: "Irlanda",
            ClientLocale.Japanese: "アイルランド",
            ClientLocale.Polish: "Irlandia",
            ClientLocale.Russian: "Ирландия",
        }
    },
    "IL": {
        "localizedNames": {
            ClientLocale.English: "Israel",
            ClientLocale.German: "Israel",
            ClientLocale.Spanish: "Israel",
            ClientLocale.French: "Israël",
            ClientLocale.Italian: "Israele",
            ClientLocale.Japanese: "イスラエル",
            ClientLocale.Polish: "Izrael",
            ClientLocale.Russian: "Израиль",
        }
    },
    "IT": {
        "localizedNames": {
            ClientLocale.English: "Italy",
            ClientLocale.German: "Italien",
            ClientLocale.Spanish: "Italia",
            ClientLocale.French: "Italie",
            ClientLocale.Italian: "Italia",
            ClientLocale.Japanese: "イタリア",
            ClientLocale.Polish: "Włochy",
            ClientLocale.Russian: "Италия",
        }
    },
    "CI": {
        "localizedNames": {
            ClientLocale.English: "Ivory Coast",
            ClientLocale.German: "Elfenbeinküste",
            ClientLocale.Spanish: "Costa de Marfil",
            ClientLocale.French: "Côte d'Ivoire",
            ClientLocale.Italian: "Costa d'Avorio",
            ClientLocale.Japanese: "コートジボワール",
            ClientLocale.Polish: "Wybrzeże Kości Słoniowej",
            ClientLocale.Russian: "Кот-д'Ивуар",
        }
    },
    "JM": {
        "localizedNames": {
            ClientLocale.English: "Jamaica",
            ClientLocale.German: "Jamaika",
            ClientLocale.Spanish: "Jamaica",
            ClientLocale.French: "Jamaïque",
            ClientLocale.Italian: "Giamaica",
            ClientLocale.Japanese: "ジャマイカ",
            ClientLocale.Polish: "Jamajka",
            ClientLocale.Russian: "Ямайка",
        }
    },
    "JP": {
        "localizedNames": {
            ClientLocale.English: "Japan",
            ClientLocale.German: "Japan",
            ClientLocale.Spanish: "Japón",
            ClientLocale.French: "Japon",
            ClientLocale.Italian: "Giappone",
            ClientLocale.Japanese: "日本",
            ClientLocale.Polish: "Japonia",
            ClientLocale.Russian: "Япония",
        }
    },
    "JO": {
        "localizedNames": {
            ClientLocale.English: "Jordan",
            ClientLocale.German: "Jordanien",
            ClientLocale.Spanish: "Jordania",
            ClientLocale.French: "Jordanie",
            ClientLocale.Italian: "Giordania",
            ClientLocale.Japanese: "ヨルダン",
            ClientLocale.Polish: "Jordania",
            ClientLocale.Russian: "Иордания",
        }
    },
    "KZ": {
        "localizedNames": {
            ClientLocale.English: "Kazakhstan",
            ClientLocale.German: "Kasachstan",
            ClientLocale.Spanish: "Kazajstán",
            ClientLocale.French: "Kazakhstan",
            ClientLocale.Italian: "Kazakistan",
            ClientLocale.Japanese: "カザフスタン",
            ClientLocale.Polish: "Kazachstan",
            ClientLocale.Russian: "Казахстан",
        }
    },
    "KE": {
        "localizedNames": {
            ClientLocale.English: "Kenya",
            ClientLocale.German: "Kenia",
            ClientLocale.Spanish: "Kenia",
            ClientLocale.French: "Kenya",
            ClientLocale.Italian: "Kenya",
            ClientLocale.Japanese: "ケニア",
            ClientLocale.Polish: "Kenia",
            ClientLocale.Russian: "Кения",
        }
    },
    "KI": {
        "localizedNames": {
            ClientLocale.English: "Kiribati",
            ClientLocale.German: "Kiribati",
            ClientLocale.Spanish: "Kiribati",
            ClientLocale.French: "Kiribati",
            ClientLocale.Italian: "Kiribati",
            ClientLocale.Japanese: "キリバス",
            ClientLocale.Polish: "Kiribati",
            ClientLocale.Russian: "Кирибати",
        }
    },
    "KR": {
        "localizedNames": {
            ClientLocale.English: "Korea",
            ClientLocale.German: "Korea",
            ClientLocale.Spanish: "Corea del Sur",
            ClientLocale.French: "Corée",
            ClientLocale.Italian: "Corea",
            ClientLocale.Japanese: "韓国",
            ClientLocale.Polish: "Korea Pn.",
            ClientLocale.Russian: "Корея",
        }
    },
    "KW": {
        "localizedNames": {
            ClientLocale.English: "Kuwait",
            ClientLocale.German: "Kuwait",
            ClientLocale.Spanish: "Kuwait",
            ClientLocale.French: "Koweït",
            ClientLocale.Italian: "Kuwait",
            ClientLocale.Japanese: "クウェート",
            ClientLocale.Polish: "Kuwejt",
            ClientLocale.Russian: "Кувейт",
        }
    },
    "KG": {
        "localizedNames": {
            ClientLocale.English: "Kyrgyz Republic",
            ClientLocale.German: "Kirgistan",
            ClientLocale.Spanish: "Kirguizistán",
            ClientLocale.French: "Kirghizistan",
            ClientLocale.Italian: "Kirghizistan",
            ClientLocale.Japanese: "キルギス",
            ClientLocale.Polish: "Kirgizja",
            ClientLocale.Russian: "Кыргызстан",
        }
    },
    "LA": {
        "localizedNames": {
            ClientLocale.English: "Lao People's Democratic Republic",
            ClientLocale.German: "Volksrepublik Laos",
            ClientLocale.Spanish: "República Democrática Popular de Laos",
            ClientLocale.French: "République populaire démocratique lao",
            ClientLocale.Italian: "Repubblica Democratica Popolare del Laos",
            ClientLocale.Japanese: "ラオス",
            ClientLocale.Polish: "Laos",
            ClientLocale.Russian: "Лаос",
        }
    },
    "LV": {
        "localizedNames": {
            ClientLocale.English: "Latvia",
            ClientLocale.German: "Lettland",
            ClientLocale.Spanish: "Letonia",
            ClientLocale.French: "Lettonie",
            ClientLocale.Italian: "Lettonia",
            ClientLocale.Japanese: "ラトビア",
            ClientLocale.Polish: "Łotwa",
            ClientLocale.Russian: "Латвия",
        }
    },
    "LB": {
        "localizedNames": {
            ClientLocale.English: "Lebanon",
            ClientLocale.German: "Libanon",
            ClientLocale.Spanish: "Líbano",
            ClientLocale.French: "Liban",
            ClientLocale.Italian: "Libano",
            ClientLocale.Japanese: "レバノン",
            ClientLocale.Polish: "Liban",
            ClientLocale.Russian: "Ливан",
        }
    },
    "LS": {
        "localizedNames": {
            ClientLocale.English: "Lesotho",
            ClientLocale.German: "Lesotho",
            ClientLocale.Spanish: "Lesotho",
            ClientLocale.French: "Lesotho",
            ClientLocale.Italian: "Lesotho",
            ClientLocale.Japanese: "レソト",
            ClientLocale.Polish: "Lesotho",
            ClientLocale.Russian: "Лесото",
        }
    },
    "LR": {
        "localizedNames": {
            ClientLocale.English: "Liberia",
            ClientLocale.German: "Liberia",
            ClientLocale.Spanish: "Liberia",
            ClientLocale.French: "Liberia",
            ClientLocale.Italian: "Liberia",
            ClientLocale.Japanese: "リベリア",
            ClientLocale.Polish: "Liberia",
            ClientLocale.Russian: "Либерия",
        }
    },
    "LI": {
        "localizedNames": {
            ClientLocale.English: "Liechtenstein",
            ClientLocale.German: "Liechtenstein",
            ClientLocale.Spanish: "Liechtenstein",
            ClientLocale.French: "Liechtenstein",
            ClientLocale.Italian: "Liechtenstein",
            ClientLocale.Japanese: "リヒテンシュタイン",
            ClientLocale.Polish: "Liechtenstein",
            ClientLocale.Russian: "Лихтенштейн",
        }
    },
    "LT": {
        "localizedNames": {
            ClientLocale.English: "Lithuania",
            ClientLocale.German: "Litauen",
            ClientLocale.Spanish: "Lituania",
            ClientLocale.French: "Lituanie",
            ClientLocale.Italian: "Lituania",
            ClientLocale.Japanese: "リトアニア",
            ClientLocale.Polish: "Litwa",
            ClientLocale.Russian: "Литва",
        }
    },
    "LU": {
        "localizedNames": {
            ClientLocale.English: "Luxembourg",
            ClientLocale.German: "Luxemburg",
            ClientLocale.Spanish: "Luxemburgo",
            ClientLocale.French: "Luxembourg",
            ClientLocale.Italian: "Lussemburgo",
            ClientLocale.Japanese: "ルクセン ブルク",
            ClientLocale.Polish: "Luksemburg",
            ClientLocale.Russian: "Люксембург",
        }
    },
    "MK": {
        "localizedNames": {
            ClientLocale.English: "Macedonia",
            ClientLocale.German: "Mazedonien",
            ClientLocale.Spanish: "Macedonia",
            ClientLocale.French: "Macédoine",
            ClientLocale.Italian: "Macedonia",
            ClientLocale.Japanese: "マケドニア",
            ClientLocale.Polish: "Macedonia",
            ClientLocale.Russian: "Македония",
        }
    },
    "MG": {
        "localizedNames": {
            ClientLocale.English: "Madagascar",
            ClientLocale.German: "Madagaskar",
            ClientLocale.Spanish: "Madagascar",
            ClientLocale.French: "Madagascar",
            ClientLocale.Italian: "Madagascar",
            ClientLocale.Japanese: "マダガスカル",
            ClientLocale.Polish: "Madagaskar",
            ClientLocale.Russian: "Мадагаскар",
        }
    },
    "MW": {
        "localizedNames": {
            ClientLocale.English: "Malawi",
            ClientLocale.German: "Malawi",
            ClientLocale.Spanish: "Malawi",
            ClientLocale.French: "Malawi",
            ClientLocale.Italian: "Malawi",
            ClientLocale.Japanese: "マラウィ",
            ClientLocale.Polish: "Malawi",
            ClientLocale.Russian: "Малави",
        }
    },
    "MY": {
        "localizedNames": {
            ClientLocale.English: "Malaysia",
            ClientLocale.German: "Malaysia",
            ClientLocale.Spanish: "Malasia",
            ClientLocale.French: "Malaisie",
            ClientLocale.Italian: "Malesia",
            ClientLocale.Japanese: "マレーシア",
            ClientLocale.Polish: "Malezja",
            ClientLocale.Russian: "Малайзия",
        }
    },
    "MV": {
        "localizedNames": {
            ClientLocale.English: "Maldives",
            ClientLocale.German: "Malediven",
            ClientLocale.Spanish: "Islas Malvinas",
            ClientLocale.French: "Maldives",
            ClientLocale.Italian: "Maldive",
            ClientLocale.Japanese: "モルディヴ",
            ClientLocale.Polish: "Malediwy",
            ClientLocale.Russian: "Мальдивские о-ва",
        }
    },
    "ML": {
        "localizedNames": {
            ClientLocale.English: "Mali",
            ClientLocale.German: "Mali",
            ClientLocale.Spanish: "Mali",
            ClientLocale.French: "Mali",
            ClientLocale.Italian: "Mali",
            ClientLocale.Japanese: " マリ",
            ClientLocale.Polish: "Mali",
            ClientLocale.Russian: "Мали",
        }
    },
    "MT": {
        "localizedNames": {
            ClientLocale.English: "Malta",
            ClientLocale.German: "Malta",
            ClientLocale.Spanish: "Malta",
            ClientLocale.French: "Malte",
            ClientLocale.Italian: "Malta",
            ClientLocale.Japanese: "マルタ",
            ClientLocale.Polish: "Malta",
            ClientLocale.Russian: "Мальта",
        }
    },
    "MH": {
        "localizedNames": {
            ClientLocale.English: "Marshall Islands",
            ClientLocale.German: "Marshall-Inseln",
            ClientLocale.Spanish: "Islas Marshall",
            ClientLocale.French: "Iles Marshall",
            ClientLocale.Italian: "Isole Marshall",
            ClientLocale.Japanese: "マーシャル諸島",
            ClientLocale.Polish: "Wyspy Marshalla",
            ClientLocale.Russian: "Маршалловы о-ва",
        }
    },
    "MQ": {
        "localizedNames": {
            ClientLocale.English: "Martinique",
            ClientLocale.German: "Martinique",
            ClientLocale.Spanish: "Martinica",
            ClientLocale.French: "Martinique",
            ClientLocale.Italian: "Martinica",
            ClientLocale.Japanese: "マルチニーク島",
            ClientLocale.Polish: "Martynika",
            ClientLocale.Russian: "О. Мартиника",
        }
    },
    "MR": {
        "localizedNames": {
            ClientLocale.English: "Mauritania",
            ClientLocale.German: "Mauretanien",
            ClientLocale.Spanish: "Mauritania",
            ClientLocale.French: "Mauritanie",
            ClientLocale.Italian: "Mauritania",
            ClientLocale.Japanese: "モーリタニア",
            ClientLocale.Polish: "Mauretania",
            ClientLocale.Russian: "Мавритания",
        }
    },
    "MU": {
        "localizedNames": {
            ClientLocale.English: "Mauritius",
            ClientLocale.German: "Mauritius",
            ClientLocale.Spanish: "Isla Mauricio",
            ClientLocale.French: "Ile Maurice",
            ClientLocale.Italian: "Mauritius",
            ClientLocale.Japanese: "モ ーリシャス",
            ClientLocale.Polish: "Mauritius",
            ClientLocale.Russian: "Маврикий",
        }
    },
    "YT": {
        "localizedNames": {
            ClientLocale.English: "Mayotte",
            ClientLocale.German: "Mayotte",
            ClientLocale.Spanish: "Mayotte",
            ClientLocale.French: "Mayotte",
            ClientLocale.Italian: "Mayotte",
            ClientLocale.Japanese: "マイヨット島",
            ClientLocale.Polish: "Mayotte",
            ClientLocale.Russian: "Майотте",
        }
    },
    "MX": {
        "localizedNames": {
            ClientLocale.English: "Mexico",
            ClientLocale.German: "Mexiko",
            ClientLocale.Spanish: "Méjico",
            ClientLocale.French: "Mexique",
            ClientLocale.Italian: "Messico",
            ClientLocale.Japanese: "メキシコ",
            ClientLocale.Polish: "Meksyk",
            ClientLocale.Russian: "Мексика",
        }
    },
    "FM": {
        "localizedNames": {
            ClientLocale.English: "Micronesia",
            ClientLocale.German: "Mikronesien",
            ClientLocale.Spanish: "Micronesia",
            ClientLocale.French: "Micronésie",
            ClientLocale.Italian: "Micronesia",
            ClientLocale.Japanese: "ミクロネシア",
            ClientLocale.Polish: "Mikronezja",
            ClientLocale.Russian: "Микронезия",
        }
    },
    "MD": {
        "localizedNames": {
            ClientLocale.English: "Moldova",
            ClientLocale.German: "Moldawien",
            ClientLocale.Spanish: "Moldavia",
            ClientLocale.French: "Moldavie",
            ClientLocale.Italian: "Moldavia",
            ClientLocale.Japanese: "モルドバ",
            ClientLocale.Polish: "Mołdawia",
            ClientLocale.Russian: "Молдова",
        }
    },
    "MC": {
        "localizedNames": {
            ClientLocale.English: "Monaco",
            ClientLocale.German: "Monaco",
            ClientLocale.Spanish: "Mónaco",
            ClientLocale.French: "Monaco",
            ClientLocale.Italian: "Monaco",
            ClientLocale.Japanese: "モナコ",
            ClientLocale.Polish: "Monako",
            ClientLocale.Russian: "Монако",
        }
    },
    "MN": {
        "localizedNames": {
            ClientLocale.English: "Mongolia",
            ClientLocale.German: "Mongolei",
            ClientLocale.Spanish: "Mongolia",
            ClientLocale.French: "Mongolie",
            ClientLocale.Italian: "Mongolia",
            ClientLocale.Japanese: "モンゴル",
            ClientLocale.Polish: "Mongolia",
            ClientLocale.Russian: "Монголия",
        }
    },
    "ME": {
        "localizedNames": {
            ClientLocale.English: "Montenegro",
            ClientLocale.German: "Montenegro",
            ClientLocale.Spanish: "Montenegro",
            ClientLocale.French: "Monténégro",
            ClientLocale.Italian: "Montenegro",
            ClientLocale.Japanese: "モンテネグロ",
            ClientLocale.Polish: "Czarnogóra",
            ClientLocale.Russian: "Черногория",
        }
    },
    "MS": {
        "localizedNames": {
            ClientLocale.English: "Montserrat",
            ClientLocale.German: "Montserrat",
            ClientLocale.Spanish: "Montserrat",
            ClientLocale.French: "Montserrat",
            ClientLocale.Italian: "Montserrat",
            ClientLocale.Japanese: "モンセラット",
            ClientLocale.Polish: "Montserrat",
            ClientLocale.Russian: "О. Монтсеррат",
        }
    },
    "MA": {
        "localizedNames": {
            ClientLocale.English: "Morocco",
            ClientLocale.German: "Marokko",
            ClientLocale.Spanish: "Marruecos",
            ClientLocale.French: "Maroc",
            ClientLocale.Italian: "Marocco",
            ClientLocale.Japanese: "モロッコ",
            ClientLocale.Polish: "Maroko",
            ClientLocale.Russian: "Марокко",
        }
    },
    "MZ": {
        "localizedNames": {
            ClientLocale.English: "Mozambique",
            ClientLocale.German: "Mosambik",
            ClientLocale.Spanish: "Mozambique",
            ClientLocale.French: "Mozambique",
            ClientLocale.Italian: "Mozambico",
            ClientLocale.Japanese: "モザンビーク",
            ClientLocale.Polish: "Mozambik",
            ClientLocale.Russian: "Мозамбик",
        }
    },
    "MM": {
        "localizedNames": {
            ClientLocale.English: "Myanmar",
            ClientLocale.German: "Myanmar",
            ClientLocale.Spanish: "Myanmar",
            ClientLocale.French: "Myanmar",
            ClientLocale.Italian: "Myanmar",
            ClientLocale.Japanese: "ミャンマー",
            ClientLocale.Polish: "Myanmar",
            ClientLocale.Russian: "Мьянма",
        }
    },
    "NA": {
        "localizedNames": {
            ClientLocale.English: "Namibia",
            ClientLocale.German: "Namibia",
            ClientLocale.Spanish: "Namibia",
            ClientLocale.French: "Namibie",
            ClientLocale.Italian: "Namibia",
            ClientLocale.Japanese: "ナミビア",
            ClientLocale.Polish: "Namibia",
            ClientLocale.Russian: "Намибия",
        }
    },
    "NR": {
        "localizedNames": {
            ClientLocale.English: "Nauru",
            ClientLocale.German: "Nauru",
            ClientLocale.Spanish: "Nauru",
            ClientLocale.French: "Nauru",
            ClientLocale.Italian: "Nauru",
            ClientLocale.Japanese: "ナウル",
            ClientLocale.Polish: "Nauru",
            ClientLocale.Russian: "Науру",
        }
    },
    "NP": {
        "localizedNames": {
            ClientLocale.English: "Nepal",
            ClientLocale.German: "Nepal",
            ClientLocale.Spanish: "Nepal",
            ClientLocale.French: "Népal",
            ClientLocale.Italian: "Nepal",
            ClientLocale.Japanese: "ネパール",
            ClientLocale.Polish: "Nepal",
            ClientLocale.Russian: "Непал",
        }
    },
    "NL": {
        "localizedNames": {
            ClientLocale.English: "Netherlands",
            ClientLocale.German: "Niederlande",
            ClientLocale.Spanish: "Países Bajos",
            ClientLocale.French: "Pays-Bas",
            ClientLocale.Italian: "Olanda",
            ClientLocale.Japanese: "オランダ",
            ClientLocale.Polish: "Niderlandy",
            ClientLocale.Russian: "Нидерланды",
        }
    },
    "AN": {
        "localizedNames": {
            ClientLocale.English: "Netherlands Antilles",
            ClientLocale.German: "Niederländische Antillen",
            ClientLocale.Spanish: "Antillas Holandesas",
            ClientLocale.French: "Antilles hollandaises",
            ClientLocale.Italian: "Antille Olandesi",
            ClientLocale.Japanese: "蘭領アンティル",
            ClientLocale.Polish: "Antyle Holenderskie",
            ClientLocale.Russian: "Антильские о-ва",
        }
    },
    "NC": {
        "localizedNames": {
            ClientLocale.English: "New Caledonia",
            ClientLocale.German: "Neukaledonien",
            ClientLocale.Spanish: "Nueva Caledonia",
            ClientLocale.French: "Nouvelle-Calédonie",
            ClientLocale.Italian: "Nuova Caledonia",
            ClientLocale.Japanese: "ニューカレドニア",
            ClientLocale.Polish: "Nowa Kaledonia",
            ClientLocale.Russian: "Новая Каледония",
        }
    },
    "NZ": {
        "localizedNames": {
            ClientLocale.English: "New Zealand",
            ClientLocale.German: "Neuseeland",
            ClientLocale.Spanish: "Nueva Zelanda",
            ClientLocale.French: "Nouvelle-Zélande",
            ClientLocale.Italian: "Nuova Zelanda",
            ClientLocale.Japanese: "ニュージーランド",
            ClientLocale.Polish: "Nowa Zelandia",
            ClientLocale.Russian: "Новая Зеландия",
        }
    },
    "NI": {
        "localizedNames": {
            ClientLocale.English: "Nicaragua",
            ClientLocale.German: "Nikaragua",
            ClientLocale.Spanish: "Nicaragua",
            ClientLocale.French: "Nicaragua",
            ClientLocale.Italian: "Nicaragua",
            ClientLocale.Japanese: "ニカラグア",
            ClientLocale.Polish: "Nikaragua",
            ClientLocale.Russian: "Никарагуа",
        }
    },
    "NE": {
        "localizedNames": {
            ClientLocale.English: "Niger",
            ClientLocale.German: "Niger",
            ClientLocale.Spanish: "Níger",
            ClientLocale.French: "Niger",
            ClientLocale.Italian: "Niger",
            ClientLocale.Japanese: "ニジェール",
            ClientLocale.Polish: "Niger",
            ClientLocale.Russian: "Нигер",
        }
    },
    "NG": {
        "localizedNames": {
            ClientLocale.English: "Nigeria",
            ClientLocale.German: "Nigeria",
            ClientLocale.Spanish: "Nigeria",
            ClientLocale.French: "Nigeria",
            ClientLocale.Italian: "Nigeria",
            ClientLocale.Japanese: "ナイジェリア",
            ClientLocale.Polish: "Nigeria",
            ClientLocale.Russian: "Нигерия",
        }
    },
    "NU": {
        "localizedNames": {
            ClientLocale.English: "Niue",
            ClientLocale.German: "Niue",
            ClientLocale.Spanish: "Niue",
            ClientLocale.French: "Niue",
            ClientLocale.Italian: "Niue",
            ClientLocale.Japanese: "ニウエ",
            ClientLocale.Polish: "Niue",
            ClientLocale.Russian: "Ниуэ",
        }
    },
    "NF": {
        "localizedNames": {
            ClientLocale.English: "Norfolk Island",
            ClientLocale.German: "Norfolk-Inseln",
            ClientLocale.Spanish: "Isla Norfolk",
            ClientLocale.French: "Iles Norfolk",
            ClientLocale.Italian: "Isola Norfolk",
            ClientLocale.Japanese: "ノーフォーク島",
            ClientLocale.Polish: "Wyspy Norfolk",
            ClientLocale.Russian: "Норфолкские о-ва",
        }
    },
    "MP": {
        "localizedNames": {
            ClientLocale.English: "Northern Mariana Islands",
            ClientLocale.German: "Nördliche Marianen",
            ClientLocale.Spanish: "Islas Marianas",
            ClientLocale.French: "Iles Marianne du Nord",
            ClientLocale.Italian: "Isole Marianne del Nord",
            ClientLocale.Japanese: "北マリアナ諸島",
            ClientLocale.Polish: "Północne Mariany",
            ClientLocale.Russian: "Северные Марианские о-ва",
        }
    },
    "NO": {
        "localizedNames": {
            ClientLocale.English: "Norway",
            ClientLocale.German: "Norwegen",
            ClientLocale.Spanish: "Noruega",
            ClientLocale.French: "Norvège",
            ClientLocale.Italian: "Norvegia",
            ClientLocale.Japanese: "ノルウェー",
            ClientLocale.Polish: "Norwegia",
            ClientLocale.Russian: "Норвегия",
        }
    },
    "OM": {
        "localizedNames": {
            ClientLocale.English: "Oman",
            ClientLocale.German: "Oman",
            ClientLocale.Spanish: "Omán",
            ClientLocale.French: "Oman",
            ClientLocale.Italian: "Oman",
            ClientLocale.Japanese: "オマーン",
            ClientLocale.Polish: "Oman",
            ClientLocale.Russian: "Оман",
        }
    },
    "PK": {
        "localizedNames": {
            ClientLocale.English: "Pakistan",
            ClientLocale.German: "Pakistan",
            ClientLocale.Spanish: "Pakistán",
            ClientLocale.French: "Pakistan",
            ClientLocale.Italian: "Pakistan",
            ClientLocale.Japanese: "パキスタン",
            ClientLocale.Polish: "Pakistan",
            ClientLocale.Russian: "Пакистан",
        }
    },
    "PW": {
        "localizedNames": {
            ClientLocale.English: "Palau",
            ClientLocale.German: "Palau",
            ClientLocale.Spanish: "Palau",
            ClientLocale.French: "Palau",
            ClientLocale.Italian: "Palau",
            ClientLocale.Japanese: "パラオ",
            ClientLocale.Polish: "Palau",
            ClientLocale.Russian: "О-ва Палау",
        }
    },
    "PS": {
        "localizedNames": {
            ClientLocale.English: "Palestinian Territory",
            ClientLocale.German: "Palästina",
            ClientLocale.Spanish: "Territorio Palestino",
            ClientLocale.French: "Territoires palestiniens",
            ClientLocale.Italian: "Territorio Palestinese",
            ClientLocale.Japanese: "パレスチナ",
            ClientLocale.Polish: "Terytorium Palestyńskie",
            ClientLocale.Russian: "Палестинская автономия",
        }
    },
    "PA": {
        "localizedNames": {
            ClientLocale.English: "Panama",
            ClientLocale.German: "Panama",
            ClientLocale.Spanish: "Panamá",
            ClientLocale.French: "Panama",
            ClientLocale.Italian: "Panama",
            ClientLocale.Japanese: "パナマ",
            ClientLocale.Polish: "Panama",
            ClientLocale.Russian: "Панама",
        }
    },
    "PG": {
        "localizedNames": {
            ClientLocale.English: "Papua New Guinea",
            ClientLocale.German: "Papua-Neuguinea",
            ClientLocale.Spanish: "Papua-Nueva Guinea",
            ClientLocale.French: "Papouasie-Nouvelle-Guinée",
            ClientLocale.Italian: "Papua Nuova Guinea",
            ClientLocale.Japanese: "パプアニューギニア",
            ClientLocale.Polish: "Papua Nowa Gwinea",
            ClientLocale.Russian: "Папуа-Новая Гвинея",
        }
    },
    "PY": {
        "localizedNames": {
            ClientLocale.English: "Paraguay",
            ClientLocale.German: "Paraguay",
            ClientLocale.Spanish: "Paraguay",
            ClientLocale.French: "Paraguay",
            ClientLocale.Italian: "Paraguay",
            ClientLocale.Japanese: "パラグアイ",
            ClientLocale.Polish: "Paragwaj",
            ClientLocale.Russian: "Парагвай",
        }
    },
    "PE": {
        "localizedNames": {
            ClientLocale.English: "Peru",
            ClientLocale.German: "Peru",
            ClientLocale.Spanish: "Perú",
            ClientLocale.French: "Pérou",
            ClientLocale.Italian: "Perù",
            ClientLocale.Japanese: "ペルー",
            ClientLocale.Polish: "Peru",
            ClientLocale.Russian: "Перу",
        }
    },
    "PH": {
        "localizedNames": {
            ClientLocale.English: "Philippines",
            ClientLocale.German: "Philippinen",
            ClientLocale.Spanish: "Filipinas",
            ClientLocale.French: "Philippines",
            ClientLocale.Italian: "Filippine",
            ClientLocale.Japanese: "フィリピン",
            ClientLocale.Polish: "Filipiny",
            ClientLocale.Russian: "Филиппины",
        }
    },
    "PN": {
        "localizedNames": {
            ClientLocale.English: "Pitcairn Island",
            ClientLocale.German: "Pitcairn-Insel",
            ClientLocale.Spanish: "Islas Pitcairn",
            ClientLocale.French: "Ile Pitcairn",
            ClientLocale.Italian: "Isole Pitcairn",
            ClientLocale.Japanese: "ピトケアン島",
            ClientLocale.Polish: "Pitcairn",
            ClientLocale.Russian: "О. Питкэрн",
        }
    },
    "PL": {
        "localizedNames": {
            ClientLocale.English: "Poland",
            ClientLocale.German: "Polen",
            ClientLocale.Spanish: "Polonia",
            ClientLocale.French: "Pologne",
            ClientLocale.Italian: "Polonia",
            ClientLocale.Japanese: "ポーランド",
            ClientLocale.Polish: "Polska",
            ClientLocale.Russian: "Польша",
        }
    },
    "PT": {
        "localizedNames": {
            ClientLocale.English: "Portugal",
            ClientLocale.German: "Portugal",
            ClientLocale.Spanish: "Portugal",
            ClientLocale.French: "Portugal",
            ClientLocale.Italian: "Portogallo",
            ClientLocale.Japanese: "ポルトガル",
            ClientLocale.Polish: "Portugalia",
            ClientLocale.Russian: "Португалия",
        }
    },
    "PR": {
        "localizedNames": {
            ClientLocale.English: "Puerto Rico",
            ClientLocale.German: "Puerto Rico",
            ClientLocale.Spanish: "Puerto Rico",
            ClientLocale.French: "Porto Rico",
            ClientLocale.Italian: "Porto Rico",
            ClientLocale.Japanese: "プエルトリコ",
            ClientLocale.Polish: "Puerto Rico",
            ClientLocale.Russian: "Пуэрто-Рико",
        }
    },
    "QA": {
        "localizedNames": {
            ClientLocale.English: "Qatar",
            ClientLocale.German: "Qatar",
            ClientLocale.Spanish: "Catar",
            ClientLocale.French: "Qatar",
            ClientLocale.Italian: "Qatar",
            ClientLocale.Japanese: "カタール",
            ClientLocale.Polish: "Katar",
            ClientLocale.Russian: "Катар",
        }
    },
    "RE": {
        "localizedNames": {
            ClientLocale.English: "Reunion",
            ClientLocale.German: "Reunion-Inseln",
            ClientLocale.Spanish: "Reunion",
            ClientLocale.French: "Réunion",
            ClientLocale.Italian: "Réunion",
            ClientLocale.Japanese: "レユニオン",
            ClientLocale.Polish: "Reunion",
            ClientLocale.Russian: "О. Реюньон",
        }
    },
    "RO": {
        "localizedNames": {
            ClientLocale.English: "Romania",
            ClientLocale.German: "Rumänien",
            ClientLocale.Spanish: "Rumanía",
            ClientLocale.French: "Roumanie",
            ClientLocale.Italian: "Romania",
            ClientLocale.Japanese: "ルーマニア",
            ClientLocale.Polish: "Rumunia",
            ClientLocale.Russian: "Румыния",
        }
    },
    "RU": {
        "localizedNames": {
            ClientLocale.English: "Russian Federation",
            ClientLocale.German: "Russische Föderation",
            ClientLocale.Spanish: "Federación rusa",
            ClientLocale.French: "Fédération de Russie",
            ClientLocale.Italian: "Federazione Russa",
            ClientLocale.Japanese: "ロシア",
            ClientLocale.Polish: "Rosja",
            ClientLocale.Russian: "Российская Федерация",
        }
    },
    "RW": {
        "localizedNames": {
            ClientLocale.English: "Rwanda",
            ClientLocale.German: "Ruanda",
            ClientLocale.Spanish: "Ruanda",
            ClientLocale.French: "Rwanda",
            ClientLocale.Italian: "Ruanda",
            ClientLocale.Japanese: "ルワンダ",
            ClientLocale.Polish: "Rwanda",
            ClientLocale.Russian: "Руанда",
        }
    },
    "WS": {
        "localizedNames": {
            ClientLocale.English: "Samoa",
            ClientLocale.German: "Samoa",
            ClientLocale.Spanish: "Samoa Occidental",
            ClientLocale.French: "Samoa",
            ClientLocale.Italian: "Samoa",
            ClientLocale.Japanese: "サモア",
            ClientLocale.Polish: "Samoa",
            ClientLocale.Russian: "Самоа",
        }
    },
    "SM": {
        "localizedNames": {
            ClientLocale.English: "San Marino",
            ClientLocale.German: "San Marino",
            ClientLocale.Spanish: "San Marino",
            ClientLocale.French: "Saint-Marin",
            ClientLocale.Italian: "San Marino",
            ClientLocale.Japanese: "サンマリノ",
            ClientLocale.Polish: "San Marino",
            ClientLocale.Russian: "Сан-Марино",
        }
    },
    "ST": {
        "localizedNames": {
            ClientLocale.English: "Sao Tome and Principe",
            ClientLocale.German: "Sao Tome und Principe",
            ClientLocale.Spanish: "Sao Tome y Príncipe",
            ClientLocale.French: "Sao Tomé et Principe",
            ClientLocale.Italian: "São Tomé e Príncipe",
            ClientLocale.Japanese: "サントメ・プリンシペ",
            ClientLocale.Polish: "Wyspa Św. Tomasza i Książęca",
            ClientLocale.Russian: "Сан-Томе и Принсипи",
        }
    },
    "SA": {
        "localizedNames": {
            ClientLocale.English: "Saudi Arabia",
            ClientLocale.German: "Saudi-Arabien",
            ClientLocale.Spanish: "Arabia Saudí",
            ClientLocale.French: "Arabie Saoudite",
            ClientLocale.Italian: "Arabia Saudita",
            ClientLocale.Japanese: "サウジアラビア",
            ClientLocale.Polish: "Arabia Saudyjska",
            ClientLocale.Russian: "Саудовская Аравия",
        }
    },
    "SN": {
        "localizedNames": {
            ClientLocale.English: "Senegal",
            ClientLocale.German: "Senegal",
            ClientLocale.Spanish: "Senegal",
            ClientLocale.French: "Sénégal",
            ClientLocale.Italian: "Senegal",
            ClientLocale.Japanese: "セネガル",
            ClientLocale.Polish: "Senegal",
            ClientLocale.Russian: "Сенегал",
        }
    },
    "RS": {
        "localizedNames": {
            ClientLocale.English: "Serbia",
            ClientLocale.German: "Serbien",
            ClientLocale.Spanish: "Serbia",
            ClientLocale.French: "Serbie",
            ClientLocale.Italian: "Serbia",
            ClientLocale.Japanese: "セルビア",
            ClientLocale.Polish: "Serbia",
            ClientLocale.Russian: "Сербия",
        }
    },
    "SC": {
        "localizedNames": {
            ClientLocale.English: "Seychelles",
            ClientLocale.German: "Seychellen",
            ClientLocale.Spanish: "Islas Seychelles",
            ClientLocale.French: "Seychelles",
            ClientLocale.Italian: "Seychelles",
            ClientLocale.Japanese: "セイシェル",
            ClientLocale.Polish: "Seszele",
            ClientLocale.Russian: "Сейшельские о-ва",
        }
    },
    "SL": {
        "localizedNames": {
            ClientLocale.English: "Sierra Leone",
            ClientLocale.German: "Sierra Leone",
            ClientLocale.Spanish: "Sierra Leona",
            ClientLocale.French: "Sierra Leone",
            ClientLocale.Italian: "Sierra Leone",
            ClientLocale.Japanese: "シエラレオネ",
            ClientLocale.Polish: "Sierra Leone",
            ClientLocale.Russian: "Сьерра-Леоне",
        }
    },
    "SG": {
        "localizedNames": {
            ClientLocale.English: "Singapore",
            ClientLocale.German: "Singapur",
            ClientLocale.Spanish: "Singapur",
            ClientLocale.French: "Singapour",
            ClientLocale.Italian: "Singapore",
            ClientLocale.Japanese: "シンガポール",
            ClientLocale.Polish: "Singapur",
            ClientLocale.Russian: "Сингапур",
        }
    },
    "SK": {
        "localizedNames": {
            ClientLocale.English: "Slovakia (Slovak Republic)",
            ClientLocale.German: "Slowakei (Slowakische Republik)",
            ClientLocale.Spanish: "Eslovaquia (República eslovaca)",
            ClientLocale.French: "Slovaquie (République slovaque)",
            ClientLocale.Italian: "Slovacchia (Repubblica Slovacca)",
            ClientLocale.Japanese: "スロバキア",
            ClientLocale.Polish: "Słowacja",
            ClientLocale.Russian: "Словакия",
        }
    },
    "SI": {
        "localizedNames": {
            ClientLocale.English: "Slovenia",
            ClientLocale.German: "Slowenien",
            ClientLocale.Spanish: "Eslovenia",
            ClientLocale.French: "Slovénie",
            ClientLocale.Italian: "Slovenia",
            ClientLocale.Japanese: "スロベニア",
            ClientLocale.Polish: "Słowenia",
            ClientLocale.Russian: "Словения",
        }
    },
    "SB": {
        "localizedNames": {
            ClientLocale.English: "Solomon Islands",
            ClientLocale.German: "Solomon-Inseln",
            ClientLocale.Spanish: "Islas de Solomón",
            ClientLocale.French: "Iles Salomon",
            ClientLocale.Italian: "Isole Salomone",
            ClientLocale.Japanese: "ソロモン諸島",
            ClientLocale.Polish: "Wyspy Salomona",
            ClientLocale.Russian: "Соломоновы о-ва",
        }
    },
    "SO": {
        "localizedNames": {
            ClientLocale.English: "Somalia",
            ClientLocale.German: "Somalia",
            ClientLocale.Spanish: "Somalia",
            ClientLocale.French: "Somalie",
            ClientLocale.Italian: "Somalia",
            ClientLocale.Japanese: "ソマリア",
            ClientLocale.Polish: "Somalia",
            ClientLocale.Russian: "Сомали",
        }
    },
    "ZA": {
        "localizedNames": {
            ClientLocale.English: "South Africa",
            ClientLocale.German: "Südafrika",
            ClientLocale.Spanish: "Sudáfrica",
            ClientLocale.French: "Afrique du Sud",
            ClientLocale.Italian: "Sudafrica",
            ClientLocale.Japanese: "南アフリカ",
            ClientLocale.Polish: "Afryka Południowa",
            ClientLocale.Russian: "ЮАР",
        }
    },
    "GS": {
        "localizedNames": {
            ClientLocale.English: "South Georgia and the South Sandwich Islands",
            ClientLocale.German: "Südgeorgien und südliche Sandwich-Inseln",
            ClientLocale.Spanish: "Georgia del Sur y las Islas Sandwich del Sur",
            ClientLocale.French: "Géorgie du Sud et les îles Sandwich du Sud",
            ClientLocale.Italian: "Georgia del sud e isole Sandwich",
            ClientLocale.Japanese: "南ジョージア・南サンドイッチ諸島",
            ClientLocale.Polish: "Południowa Georgia i Sandwich Południowy",
            ClientLocale.Russian: "Южн. Георгия и Южн. Сандв. о-ва",
        }
    },
    "ES": {
        "localizedNames": {
            ClientLocale.English: "Spain",
            ClientLocale.German: "Spanien",
            ClientLocale.Spanish: "España",
            ClientLocale.French: "Espagne",
            ClientLocale.Italian: "Spagna",
            ClientLocale.Japanese: "スペイン",
            ClientLocale.Polish: "Hiszpania",
            ClientLocale.Russian: "Испания",
        }
    },
    "LK": {
        "localizedNames": {
            ClientLocale.English: "Sri Lanka",
            ClientLocale.German: "Sri Lanka",
            ClientLocale.Spanish: "Sri Lanka",
            ClientLocale.French: "Sri Lanka",
            ClientLocale.Italian: "Sri Lanka",
            ClientLocale.Japanese: "スリランカ",
            ClientLocale.Polish: "Sri Lanka",
            ClientLocale.Russian: "Шри-Ланка",
        }
    },
    "SH": {
        "localizedNames": {
            ClientLocale.English: "St. Helena",
            ClientLocale.German: "St. Helena",
            ClientLocale.Spanish: "Sta. Helena",
            ClientLocale.French: "Ste-Hélène",
            ClientLocale.Italian: "St. Helena",
            ClientLocale.Japanese: "セントヘレナ島",
            ClientLocale.Polish: "Wyspa Św. Heleny",
            ClientLocale.Russian: "О. Св. Елены",
        }
    },
    "KN": {
        "localizedNames": {
            ClientLocale.English: "St. Kitts and Nevis",
            ClientLocale.German: "St. Kitts und Nevis",
            ClientLocale.Spanish: "San Kitts y Nevis",
            ClientLocale.French: "Saint-Kitts-et-Nevis",
            ClientLocale.Italian: "St. Kitts e Nevis",
            ClientLocale.Japanese: "セントキッツ・ネイビス",
            ClientLocale.Polish: "St.Kitts and Nevis",
            ClientLocale.Russian: "Сент-Китс\xa0и\xa0Невис",
        }
    },
    "LC": {
        "localizedNames": {
            ClientLocale.English: "St. Lucia",
            ClientLocale.German: "St. Lucia",
            ClientLocale.Spanish: "Sta. Lucía",
            ClientLocale.French: "Sainte Lucie",
            ClientLocale.Italian: "St. Lucia",
            ClientLocale.Japanese: "セントルシア",
            ClientLocale.Polish: "St. Lucia",
            ClientLocale.Russian: "Сент-Люсия",
        }
    },
    "PM": {
        "localizedNames": {
            ClientLocale.English: "St. Pierre and Miquelon",
            ClientLocale.German: "St. Pierre und Miquelon",
            ClientLocale.Spanish: "San Pierre y Miquelon",
            ClientLocale.French: "St-Pierre-et-Miquelon",
            ClientLocale.Italian: "St. Pierre e Miquelon",
            ClientLocale.Japanese: "サンピエール・ミクロン",
            ClientLocale.Polish: "St. Pierre and Miquelon",
            ClientLocale.Russian: "О-ва Сен-Пьер и Микелон",
        }
    },
    "VC": {
        "localizedNames": {
            ClientLocale.English: "St. Vincent and the Grenadines",
            ClientLocale.German: "St. Vincent und die Grenadinen",
            ClientLocale.Spanish: "San Vincente y Granadinas",
            ClientLocale.French: "Saint-Vincent-et-Grenadines",
            ClientLocale.Italian: "St. Vincent e Grenadine",
            ClientLocale.Japanese: "セントビンセント・グレナディーン",
            ClientLocale.Polish: "St.Vincent i Grenadyny",
            ClientLocale.Russian: "Сент-Винсент\xa0и\xa0Гренадины",
        }
    },
    "SR": {
        "localizedNames": {
            ClientLocale.English: "Suriname",
            ClientLocale.German: "Surinam",
            ClientLocale.Spanish: "Surinam",
            ClientLocale.French: "Surinam",
            ClientLocale.Italian: "Suriname",
            ClientLocale.Japanese: "スリナム",
            ClientLocale.Polish: "Surinam",
            ClientLocale.Russian: "Суринам",
        }
    },
    "SJ": {
        "localizedNames": {
            ClientLocale.English: "Svalbard and Jan Mayen Islands",
            ClientLocale.German: "Svalbard- und Jan Mayen-Inseln",
            ClientLocale.Spanish: "Islas Svalbard y Jan Mayen",
            ClientLocale.French: "Iles Svalbard et Jan Mayen",
            ClientLocale.Italian: "Isole Svalbard e Jan Mayen",
            ClientLocale.Japanese: "スバールバル諸島",
            ClientLocale.Polish: "Wyspy Svalbard i Jan Mayen",
            ClientLocale.Russian: "Шпицберген",
        }
    },
    "SZ": {
        "localizedNames": {
            ClientLocale.English: "Swaziland",
            ClientLocale.German: "Swasiland",
            ClientLocale.Spanish: "Swazilandia",
            ClientLocale.French: "Swaziland",
            ClientLocale.Italian: "Swaziland",
            ClientLocale.Japanese: "スワジランド",
            ClientLocale.Polish: "Suazi",
            ClientLocale.Russian: "Свазиленд",
        }
    },
    "SE": {
        "localizedNames": {
            ClientLocale.English: "Sweden",
            ClientLocale.German: "Schweden",
            ClientLocale.Spanish: "Suecia",
            ClientLocale.French: "Suède",
            ClientLocale.Italian: "Svezia",
            ClientLocale.Japanese: "スウェーデン",
            ClientLocale.Polish: "Szwecja",
            ClientLocale.Russian: "Швеция",
        }
    },
    "CH": {
        "localizedNames": {
            ClientLocale.English: "Switzerland",
            ClientLocale.German: "Schweiz",
            ClientLocale.Spanish: "Suiza",
            ClientLocale.French: "Suisse",
            ClientLocale.Italian: "Svizzera",
            ClientLocale.Japanese: "スイス",
            ClientLocale.Polish: "Szwajcaria",
            ClientLocale.Russian: "Швейцария",
        }
    },
    "TW": {
        "localizedNames": {
            ClientLocale.English: "Taiwan",
            ClientLocale.German: "Taiwan",
            ClientLocale.Spanish: "Taiwan",
            ClientLocale.French: "Taiwan",
            ClientLocale.Italian: "Taiwan",
            ClientLocale.Japanese: "台湾",
            ClientLocale.Polish: "Tajwan",
            ClientLocale.Russian: "Тайвань",
        }
    },
    "TJ": {
        "localizedNames": {
            ClientLocale.English: "Tajikistan",
            ClientLocale.German: "Tadschikistan",
            ClientLocale.Spanish: "Tadjikistán",
            ClientLocale.French: "Tadjikistan",
            ClientLocale.Italian: "Tagikistan",
            ClientLocale.Japanese: "タジキスタ ン",
            ClientLocale.Polish: "Tadżykistan",
            ClientLocale.Russian: "Таджикистан",
        }
    },
    "TZ": {
        "localizedNames": {
            ClientLocale.English: "Tanzania",
            ClientLocale.German: "Tansania",
            ClientLocale.Spanish: "Tanzania",
            ClientLocale.French: "Tanzanie",
            ClientLocale.Italian: "Tanzania",
            ClientLocale.Japanese: "タンザニア",
            ClientLocale.Polish: "Tanzania",
            ClientLocale.Russian: "Танзания",
        }
    },
    "TH": {
        "localizedNames": {
            ClientLocale.English: "Thailand",
            ClientLocale.German: "Thailand",
            ClientLocale.Spanish: "Tailandia",
            ClientLocale.French: "Thaïlande",
            ClientLocale.Italian: "Thailandia",
            ClientLocale.Japanese: "タイ",
            ClientLocale.Polish: "Tajlandia",
            ClientLocale.Russian: "Тайланд",
        }
    },
    "TG": {
        "localizedNames": {
            ClientLocale.English: "Togo",
            ClientLocale.German: "Togo",
            ClientLocale.Spanish: "Togo",
            ClientLocale.French: "Togo",
            ClientLocale.Italian: "Togo",
            ClientLocale.Japanese: "トーゴ",
            ClientLocale.Polish: "Togo",
            ClientLocale.Russian: "Того",
        }
    },
    "TK": {
        "localizedNames": {
            ClientLocale.English: "Tokelau",
            ClientLocale.German: "Tokelau",
            ClientLocale.Spanish: "Tokelau",
            ClientLocale.French: "Tokelau",
            ClientLocale.Italian: "Tokelau",
            ClientLocale.Japanese: "トケラウ諸島",
            ClientLocale.Polish: "Tokelau",
            ClientLocale.Russian: "О-ва Токелау",
        }
    },
    "TO": {
        "localizedNames": {
            ClientLocale.English: "Tonga",
            ClientLocale.German: "Tonga",
            ClientLocale.Spanish: "Tonga",
            ClientLocale.French: "Tonga",
            ClientLocale.Italian: "Tonga",
            ClientLocale.Japanese: "トンガ",
            ClientLocale.Polish: "Tonga",
            ClientLocale.Russian: "Тонга",
        }
    },
    "TT": {
        "localizedNames": {
            ClientLocale.English: "Trinidad and Tobago",
            ClientLocale.German: "Trinidad und Tobago",
            ClientLocale.Spanish: "Trinidad y Tobago",
            ClientLocale.French: "Trinité-et-Tobago",
            ClientLocale.Italian: "Trinidad e Tobago",
            ClientLocale.Japanese: "トリニダード・トバゴ",
            ClientLocale.Polish: "Trynidad i Tobago",
            ClientLocale.Russian: "Тринидад и Тобаго",
        }
    },
    "TN": {
        "localizedNames": {
            ClientLocale.English: "Tunisia",
            ClientLocale.German: "Tunesien",
            ClientLocale.Spanish: "Túnez",
            ClientLocale.French: "Tunisie",
            ClientLocale.Italian: "Tunisia",
            ClientLocale.Japanese: "チュニジア",
            ClientLocale.Polish: "Tunezja",
            ClientLocale.Russian: "Тунис",
        }
    },
    "TR": {
        "localizedNames": {
            ClientLocale.English: "Turkey",
            ClientLocale.German: "Türkei",
            ClientLocale.Spanish: "Turquía",
            ClientLocale.French: "Turquie",
            ClientLocale.Italian: "Turchia",
            ClientLocale.Japanese: " トルコ",
            ClientLocale.Polish: "Turcja",
            ClientLocale.Russian: "Турция",
        }
    },
    "TM": {
        "localizedNames": {
            ClientLocale.English: "Turkmenistan",
            ClientLocale.German: "Turkmenistan",
            ClientLocale.Spanish: "Turkmenistan",
            ClientLocale.French: "Turkménistan",
            ClientLocale.Italian: "Turkmenistan",
            ClientLocale.Japanese: "トルクメニスタン",
            ClientLocale.Polish: "Turkmenistan",
            ClientLocale.Russian: "Туркменистан",
        }
    },
    "TC": {
        "localizedNames": {
            ClientLocale.English: "Turks and Caicos Islands",
            ClientLocale.German: "Turks- und Caicos-Inseln",
            ClientLocale.Spanish: "Turks y Caicos",
            ClientLocale.French: "Iles Turks et Caicos",
            ClientLocale.Italian: "Isole Turks e Caicos",
            ClientLocale.Japanese: "タークス・カイコス諸島",
            ClientLocale.Polish: "Wyspy Turks i Caicos",
            ClientLocale.Russian: "О-ва Теркс и Кайкос",
        }
    },
    "TV": {
        "localizedNames": {
            ClientLocale.English: "Tuvalu",
            ClientLocale.German: "Tuvalu",
            ClientLocale.Spanish: "Tuvalu",
            ClientLocale.French: "Tuvalu",
            ClientLocale.Italian: "Tuvalu",
            ClientLocale.Japanese: "ツバル",
            ClientLocale.Polish: "Tuvalu",
            ClientLocale.Russian: "Тувалу",
        }
    },
    "UG": {
        "localizedNames": {
            ClientLocale.English: "Uganda",
            ClientLocale.German: "Uganda",
            ClientLocale.Spanish: "Uganda",
            ClientLocale.French: "Ouganda",
            ClientLocale.Italian: "Uganda",
            ClientLocale.Japanese: "ウガンダ",
            ClientLocale.Polish: "Uganda",
            ClientLocale.Russian: "Уганда",
        }
    },
    "UA": {
        "localizedNames": {
            ClientLocale.English: "Ukraine",
            ClientLocale.German: "Ukraine",
            ClientLocale.Spanish: "Ucrania",
            ClientLocale.French: "Ukraine",
            ClientLocale.Italian: "Ucraina",
            ClientLocale.Japanese: "ウクライナ",
            ClientLocale.Polish: "Ukraina",
            ClientLocale.Russian: "Украина",
        }
    },
    "AE": {
        "localizedNames": {
            ClientLocale.English: "United Arab Emirates",
            ClientLocale.German: "Vereinigte Arabische Emirate",
            ClientLocale.Spanish: "Emiratos Árabes Unidos",
            ClientLocale.French: "Emirats arabes unis",
            ClientLocale.Italian: "Emirati Arabi Uniti",
            ClientLocale.Japanese: "アラブ首長国連邦",
            ClientLocale.Polish: "Zjednoczone Emiraty Arabskie",
            ClientLocale.Russian: "ОАЭ",
        }
    },
    "GB": {
        "localizedNames": {
            ClientLocale.English: "United Kingdom",
            ClientLocale.German: "Großbritannien",
            ClientLocale.Spanish: "Reino Unido",
            ClientLocale.French: "Grande-Bretagne",
            ClientLocale.Italian: "Regno Unito",
            ClientLocale.Japanese: "イギリス",
            ClientLocale.Polish: "Wielka Brytania",
            ClientLocale.Russian: "Великобритания",
        }
    },
    "UM": {
        "localizedNames": {
            ClientLocale.English: "United States Minor Outlying Islands",
            ClientLocale.German: "Kleinere US-Inseln außerhalb der USA",
            ClientLocale.Spanish: "Islas exteriores menores de EE.UU.",
            ClientLocale.French: "Iles Mineures Américaines",
            ClientLocale.Italian: "Isole esterne minori USA",
            ClientLocale.Japanese: "米辺境諸島",
            ClientLocale.Polish: "Sporady Środkowopolinezyjskie",
            ClientLocale.Russian: "Малые о-ва США",
        }
    },
    "US": {
        "localizedNames": {
            ClientLocale.English: "United States of America",
            ClientLocale.German: "Vereinigte Staaten",
            ClientLocale.Spanish: "Estados Unidos",
            ClientLocale.French: "Etats-Unis d'Amérique",
            ClientLocale.Italian: "Stati Uniti d'America",
            ClientLocale.Japanese: "アメリカ合衆国",
            ClientLocale.Polish: "USA",
            ClientLocale.Russian: "США",
        },
        "allowEmailsDefaultValue": True,
    },
    "UY": {
        "localizedNames": {
            ClientLocale.English: "Uruguay",
            ClientLocale.German: "Uruguay",
            ClientLocale.Spanish: "Uruguay",
            ClientLocale.French: "Uruguay",
            ClientLocale.Italian: "Uruguay",
            ClientLocale.Japanese: "ウルグアイ",
            ClientLocale.Polish: "Urugwaj",
            ClientLocale.Russian: "Уругвай",
        }
    },
    "VI": {
        "localizedNames": {
            ClientLocale.English: "US Virgin Islands",
            ClientLocale.German: "Jungfraueninseln (USA)",
            ClientLocale.Spanish: "Islas Vírgenes de los EE.UU.",
            ClientLocale.French: "Iles Vierges des Etats-Unis",
            ClientLocale.Italian: "Isole Vergini degli Stati Uniti",
            ClientLocale.Japanese: "米領バージン諸島",
            ClientLocale.Polish: "Wyspy Dziewicze Stanów Zjednoczonych",
            ClientLocale.Russian: "Виргинские о-ва (США)",
        }
    },
    "UZ": {
        "localizedNames": {
            ClientLocale.English: "Uzbekistan",
            ClientLocale.German: "Usbekistan",
            ClientLocale.Spanish: "Uzbekistan",
            ClientLocale.French: "Ouzbékistan",
            ClientLocale.Italian: "Uzbekistan",
            ClientLocale.Japanese: "ウズべキスタン",
            ClientLocale.Polish: "Uzbekistan",
            ClientLocale.Russian: "Узбекистан",
        }
    },
    "VU": {
        "localizedNames": {
            ClientLocale.English: "Vanuatu",
            ClientLocale.German: "Vanuatu",
            ClientLocale.Spanish: "Vanuatu",
            ClientLocale.French: "Vanuatu",
            ClientLocale.Italian: "Vanuatu",
            ClientLocale.Japanese: "バヌアツ",
            ClientLocale.Polish: "Vanuatu",
            ClientLocale.Russian: "Вануату",
        }
    },
    "VA": {
        "localizedNames": {
            ClientLocale.English: "Vatican City",
            ClientLocale.German: "Vatikan",
            ClientLocale.Spanish: "Ciudad del Vaticano",
            ClientLocale.French: "Cité du Vatican",
            ClientLocale.Italian: "Città del Vaticano",
            ClientLocale.Japanese: "バチカン市国",
            ClientLocale.Polish: "Watykan",
            ClientLocale.Russian: "Ватикан",
        }
    },
    "VE": {
        "localizedNames": {
            ClientLocale.English: "Venezuela",
            ClientLocale.German: "Venezuela",
            ClientLocale.Spanish: "Venezuela",
            ClientLocale.French: "Venezuela",
            ClientLocale.Italian: "Venezuela",
            ClientLocale.Japanese: "ベネズエラ",
            ClientLocale.Polish: "Wenezuela",
            ClientLocale.Russian: "Венесуэла",
        }
    },
    "VN": {
        "localizedNames": {
            ClientLocale.English: "Vietnam",
            ClientLocale.German: "Vietnam",
            ClientLocale.Spanish: "Vietnam",
            ClientLocale.French: "Viêtnam",
            ClientLocale.Italian: "Vietnam",
            ClientLocale.Japanese: "ベトナム",
            ClientLocale.Polish: "Wietnam",
            ClientLocale.Russian: "Вьетнам",
        }
    },
    "WF": {
        "localizedNames": {
            ClientLocale.English: "Wallis and Futuna Islands",
            ClientLocale.German: "Wallis- und Futuna-Inseln",
            ClientLocale.Spanish: "Wallis y Futuna",
            ClientLocale.French: "Wallis et Futuna",
            ClientLocale.Italian: "Wallis e Futuna",
            ClientLocale.Japanese: "ワリス・フテュナ諸島",
            ClientLocale.Polish: "Wallis i Futuna",
            ClientLocale.Russian: "О-ва Уоллис и Футуна",
        }
    },
    "EH": {
        "localizedNames": {
            ClientLocale.English: "Western Sahara",
            ClientLocale.German: "Westsahara",
            ClientLocale.Spanish: "Sahara Occidental",
            ClientLocale.French: "Sahara occidental",
            ClientLocale.Italian: "Sahara Occidentale",
            ClientLocale.Japanese: "西サハラ",
            ClientLocale.Polish: "Zachodnia Sahara",
            ClientLocale.Russian: "Западная Сахара",
        }
    },
    "YE": {
        "localizedNames": {
            ClientLocale.English: "Yemen",
            ClientLocale.German: "Jemen",
            ClientLocale.Spanish: "Yemen",
            ClientLocale.French: "Yémen",
            ClientLocale.Italian: "Yemen",
            ClientLocale.Japanese: "イエメン",
            ClientLocale.Polish: "Jemen",
            ClientLocale.Russian: "Йемен",
        }
    },
    "ZM": {
        "localizedNames": {
            ClientLocale.English: "Zambia",
            ClientLocale.German: "Sambia",
            ClientLocale.Spanish: "Zambia",
            ClientLocale.French: "Zambie",
            ClientLocale.Italian: "Zambia",
            ClientLocale.Japanese: "ザンビア",
            ClientLocale.Polish: "Zambia",
            ClientLocale.Russian: "Замбия",
        }
    },
    "ZW": {
        "localizedNames": {
            ClientLocale.English: "Zimbabwe",
            ClientLocale.German: "Zimbabwe",
            ClientLocale.Spanish: "Zimbabwe",
            ClientLocale.French: "Zimbabwe",
            ClientLocale.Italian: "Zimbabwe",
            ClientLocale.Japanese: "ジンバブエ",
            ClientLocale.Polish: "Zimbabwe",
            ClientLocale.Russian: "Зимбабве",
        }
    },
}


@lru_cache
def getLocalizedCountryList(locale: ClientLocale):
    # Get the list of countries in the specified locale

    # Return the list of countries in specified format:
    # {
    #    "ISOCode": "DBG",
    #    "description": "Debugistan"
    # }
    #
    # Country can have these optional values:
    # allowEmailsDefaultValue [boolean]
    # parentalControlAgeLimit [int]
    # registrationAgeLimit [int]
    #
    # If the country has a localized name, it will be used. Otherwise, the English name will be used.

    countries = []

    for isoCode, countryData in COUNTRY_LIST.items():
        localizedNames = countryData["localizedNames"]
        countryName = localizedNames.get(locale, localizedNames[ClientLocale.English])

        country = {"ISOCode": isoCode, "description": countryName}

        if "allowEmailsDefaultValue" in countryData:
            country["allowEmailsDefaultValue"] = countryData["allowEmailsDefaultValue"]

        if "parentalControlAgeLimit" in countryData:
            country["parentalControlAgeLimit"] = countryData["parentalControlAgeLimit"]

        if "registrationAgeLimit" in countryData:
            country["registrationAgeLimit"] = countryData["registrationAgeLimit"]

        countries.append(country)

    # Sort the countries by name
    countries.sort(key=lambda x: x["description"])
    return countries
