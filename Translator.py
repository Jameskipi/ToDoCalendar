def translate_month(number, language):
    if language == "PL":
        match number:
            case 1:
                return "Styczeń"
            case 2:
                return "Luty"
            case 3:
                return "Marzec"
            case 4:
                return "Kwiecień"
            case 5:
                return "Maj"
            case 6:
                return "Czerwiec"
            case 7:
                return "Lipiec"
            case 8:
                return "Sierpień"
            case 9:
                return "Wrzesień"
            case 10:
                return "Październik"
            case 11:
                return "Listopad"
            case 12:
                return "Grudzień"

    match number:
        case 1:
            return "January"
        case 2:
            return "February"
        case 3:
            return "March"
        case 4:
            return "April"
        case 5:
            return "May"
        case 6:
            return "June"
        case 7:
            return "July"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "October"
        case 11:
            return "November"
        case 12:
            return "December"


def translate_menu(number, language):
    if language == "PL":
        match number:
            case -1:
                return "Ten miesiąc"
            case 0:
                return "Najbliższe 7 dni"
            case 1:
                return "Następny miesiąc"

    match number:
        case -1:
            return "This month"
        case 0:
            return "Next 7 days"
        case 1:
            return "Next month"
