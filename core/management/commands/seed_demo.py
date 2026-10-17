from datetime import time
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from blog.models import Category, Post
from core.models import FAQ, OpeningHours, SiteSettings, Testimonial
from services.models import Service, ServiceCategory, ServiceImage
from team.models import Specialty, TeamMember
from training.models import ClassSession, GymClass, MembershipPlan

SEED_ASSETS = Path(settings.BASE_DIR) / "seed_assets"


SITE = {
    "name": "FORGE Fitness Studio",
    "tagline_mk": "Сила, кондиција и заедница во срцето на Скопје.",
    "tagline_en": "Strength, conditioning and community in the heart of Skopje.",
    "short_about_mk": (
        "FORGE е студио за сила и кондиција во Скопје. Работиме со луѓе кои "
        "сакаат да тренираат паметно — со јасен план, стручен надзор и без "
        "притисок. Секој член добива програма прилагодена на своите цели."
    ),
    "short_about_en": (
        "FORGE is a strength and conditioning studio in Skopje. We work with "
        "people who want to train properly — with a clear plan, qualified "
        "coaching and no pressure. Every member gets a programme built around "
        "their own goals."
    ),
    "street_mk": "Бул. Партизански одреди 62",
    "street_en": "62 Partizanski Odredi Blvd",
    "city_mk": "Скопје",
    "city_en": "Skopje",
    "postal_code": "1000",
    "phone": "+389 2 3092 400",
    "email": "info@forgefitness.mk",
    "facebook": "https://www.facebook.com/",
    "instagram": "https://www.instagram.com/",
    "youtube": "https://www.youtube.com/",
    "map_lat": 42.0030,
    "map_lng": 21.4008,
}

HOURS = [
    (0, time(6, 0), time(23, 0), False),
    (1, time(6, 0), time(23, 0), False),
    (2, time(6, 0), time(23, 0), False),
    (3, time(6, 0), time(23, 0), False),
    (4, time(6, 0), time(22, 0), False),
    (5, time(8, 0), time(21, 0), False),
    (6, time(9, 0), time(18, 0), False),
]

SERVICE_CATEGORIES = [
    ("coaching", "Коучинг", "Coaching", 1),
    ("health", "Здравје и опоравување", "Health & recovery", 2),
    ("extra", "Дополнителни услуги", "Additional services", 3),
]

SERVICES = [
    {
        "slug": "personalen-trening",
        "cat": "coaching",
        "icon": "bi-person-arms-up",
        "featured": True,
        "price": 1200,
        "duration": 60,
        "mk": (
            "Персонален тренинг",
            "Тренинг еден на еден со тренер кој ја пишува твојата програма.",
            "Персоналниот тренинг е најбрзиот начин да научиш правилна техника и "
            "да напредуваш без застој. Пред првиот тренинг правиме проценка на "
            "движењето, ги дефинираме целите и составуваме програма за наредните "
            "дванаесет недели. На секои четири недели ја ревидираме програмата "
            "според твојот напредок.",
            "Почетна проценка на движење\nИндивидуална програма за 12 недели\n"
            "Корекција на техника на секој тренинг\nРевизија на програмата на 4 недели\n"
            "Пристап до апликацијата за следење напредок",
        ),
        "en": (
            "Personal training",
            "One-to-one sessions with a coach who writes your programme.",
            "Personal training is the fastest way to learn correct technique and "
            "keep progressing without plateaus. Before your first session we "
            "assess your movement, agree your goals and build a twelve-week "
            "programme. Every four weeks we review and adjust it based on your "
            "actual progress.",
            "Initial movement assessment\nIndividual 12-week programme\n"
            "Technique correction every session\nProgramme review every 4 weeks\n"
            "Access to the progress tracking app",
        ),
    },
    {
        "slug": "programa-za-sila",
        "cat": "coaching",
        "icon": "bi-trophy",
        "featured": True,
        "price": 2500,
        "duration": None,
        "mk": (
            "Програма за сила",
            "Структурирана дванаесетнеделна програма за чучањ, потисок и мртво кревање.",
            "Ако веќе тренираш но напредокот застанал, оваа програма е за тебе. "
            "Работиме со проверени модели на периодизација, со јасни бројки за "
            "секоја недела. Не мора да доаѓаш на персонални тренинзи — програмата "
            "ја добиваш напишана, а еднаш месечно правиме проверка на техниката.",
            "Периодизирана програма за 12 недели\nЈасни оптоварувања за секоја недела\n"
            "Месечна проверка на техника во студиото\nПоддршка преку порака во работни денови\n"
            "Тест на максимална сила на крајот од циклусот",
        ),
        "en": (
            "Strength programming",
            "A structured twelve-week plan for the squat, press and deadlift.",
            "If you already train but progress has stalled, this is for you. We "
            "use proven periodisation models with concrete numbers for every "
            "week. You don't need to book personal sessions — the programme is "
            "written for you, with a monthly technique check in the studio.",
            "Periodised 12-week programme\nExact loads prescribed for every week\n"
            "Monthly technique check in the studio\nMessage support on working days\n"
            "Max strength test at the end of the cycle",
        ),
    },
    {
        "slug": "nutricionistichko-sovetuvanje",
        "cat": "health",
        "icon": "bi-egg-fried",
        "featured": True,
        "price": 1800,
        "duration": 45,
        "mk": (
            "Нутриционистичко советување",
            "План за исхрана што се вклопува во твојот живот, без забранети намирници.",
            "Нема чудесни диети и нема листа на забранета храна. Тргнуваме од тоа "
            "што веќе јадеш, го мериме внесот една недела и потоа правиме мали "
            "промени кои можеш да ги одржиш. Соработуваме со сертифициран "
            "нутриционист, а планот се прилагодува на твојот распоред и буџет.",
            "Анализа на тековната исхрана\nПерсонализиран план за макронутриенти\n"
            "Предлози за оброци и листа за пазарење\nКонтролна средба на две недели\n"
            "Поддршка за јадење надвор и патувања",
        ),
        "en": (
            "Nutrition coaching",
            "An eating plan that fits your life, with no forbidden foods.",
            "No miracle diets and no banned-food lists. We start from what you "
            "already eat, track it for a week, then make small changes you can "
            "actually sustain. Delivered with a certified nutritionist and "
            "adapted to your schedule and your budget.",
            "Analysis of your current diet\nPersonalised macronutrient plan\n"
            "Meal suggestions and a shopping list\nFollow-up session every two weeks\n"
            "Guidance for eating out and travelling",
        ),
    },
    {
        "slug": "fitnes-procenka",
        "cat": "health",
        "icon": "bi-clipboard-pulse",
        "featured": False,
        "price": 900,
        "duration": 60,
        "mk": (
            "Фитнес проценка",
            "Детална проценка на состав на телото, движење и кондиција.",
            "Проценката трае еден час и дава јасна појдовна точка. Мериме состав "
            "на телото, тестираме подвижност на зглобовите, ја оценуваме "
            "стабилноста на трупот и правиме тест на аеробна кондиција. На крајот "
            "добиваш писмен извештај со препораки.",
            "Мерење на состав на телото\nСкрининг на подвижност\nТест на аеробна кондиција\n"
            "Писмен извештај со препораки\nБесплатно повторување по 12 недели",
        ),
        "en": (
            "Fitness assessment",
            "A detailed check of body composition, movement and conditioning.",
            "The assessment takes an hour and gives you a clear starting point. "
            "We measure body composition, screen joint mobility, assess trunk "
            "stability and run an aerobic fitness test. You leave with a written "
            "report and recommendations.",
            "Body composition measurement\nMobility screening\nAerobic fitness test\n"
            "Written report with recommendations\nFree retest after 12 weeks",
        ),
    },
    {
        "slug": "sportska-masaza",
        "cat": "health",
        "icon": "bi-heart-pulse",
        "featured": False,
        "price": 1400,
        "duration": 50,
        "mk": (
            "Спортска масажа",
            "Третман за опоравување помеѓу тешки тренинзи.",
            "Спортската масажа помага да се намали мускулната напнатост и да се "
            "забрза опоравувањето. Терапевтот работи целно на групите мускули "
            "што ги оптоваруваш најмногу. Препорачуваме еден третман на две "
            "недели во периоди на интензивен тренинг.",
            "Целна работа на оптоварените мускули\nТехники за опоравување\n"
            "Совети за домашно растегнување\nМоже да се комбинира со мобилност",
        ),
        "en": (
            "Sports massage",
            "Recovery treatment between hard training blocks.",
            "Sports massage reduces muscular tension and speeds up recovery. The "
            "therapist works specifically on the muscle groups you load most. We "
            "recommend one treatment every two weeks during intensive training "
            "periods.",
            "Targeted work on loaded muscles\nRecovery techniques\n"
            "Home stretching guidance\nCan be combined with mobility work",
        ),
    },
    {
        "slug": "rehabilitacija-i-mobilnost",
        "cat": "health",
        "icon": "bi-bandaid",
        "featured": False,
        "price": 1600,
        "duration": 50,
        "mk": (
            "Рехабилитација и мобилност",
            "Враќање на тренинг по повреда, во соработка со физиотерапевт.",
            "Работиме со луѓе кои се враќаат на тренинг по повреда на колено, "
            "рамо или грб. Програмата се прави заедно со физиотерапевт и се "
            "движи постепено — од контролирано движење, преку враќање на силата, "
            "до целосно оптоварување.",
            "Проценка во соработка со физиотерапевт\nПостепена програма за враќање\n"
            "Вежби за домашно изведување\nЈасни критериуми за следна фаза",
        ),
        "en": (
            "Rehab & mobility",
            "Returning to training after injury, alongside a physiotherapist.",
            "We work with people coming back from knee, shoulder or back "
            "injuries. The programme is built together with a physiotherapist "
            "and progresses gradually — from controlled movement, through "
            "rebuilding strength, to full loading.",
            "Assessment together with a physiotherapist\nGradual return-to-training plan\n"
            "Exercises to do at home\nClear criteria for progressing to the next stage",
        ),
    },
    {
        "slug": "onlajn-kouching",
        "cat": "extra",
        "icon": "bi-laptop",
        "featured": False,
        "price": 2000,
        "duration": None,
        "mk": (
            "Онлајн коучинг",
            "Истата програма и поддршка, без да мора да доаѓаш во студиото.",
            "За членови кои патуваат или живеат надвор од Скопје. Програмата ја "
            "добиваш преку апликација, снимаш видео од вежбите, а тренерот дава "
            "повратна информација за техниката. Еднаш неделно имаме видео повик.",
            "Програма преку апликација\nВидео анализа на техниката\n"
            "Неделен видео повик со тренер\nПрилагодување според достапна опрема",
        ),
        "en": (
            "Online coaching",
            "The same programme and support without coming to the studio.",
            "For members who travel or live outside Skopje. You get the "
            "programme through an app, film your lifts, and your coach gives "
            "feedback on technique. We have a video call once a week.",
            "Programme delivered through an app\nVideo technique analysis\n"
            "Weekly video call with your coach\nAdapted to the equipment you have",
        ),
    },
    {
        "slug": "korporativni-treninzi",
        "cat": "extra",
        "icon": "bi-people",
        "featured": False,
        "price": 8000,
        "duration": 60,
        "mk": (
            "Корпоративни тренинзи",
            "Групни тренинзи за компании, во студиото или во вашиот простор.",
            "Организираме редовни групни тренинзи за тимови од 8 до 20 луѓе. "
            "Тренинзите се прилагодуваат на нивото на групата и може да се "
            "одржуваат во нашето студио или во вашиот деловен простор.",
            "Групи од 8 до 20 луѓе\nПрилагодено на нивото на групата\n"
            "Во студиото или кај вас\nМесечен извештај за присутност\nПопуст за годишен договор",
        ),
        "en": (
            "Corporate training",
            "Group sessions for companies, in the studio or at your offices.",
            "We run regular group sessions for teams of 8 to 20 people. Sessions "
            "are adapted to the level of the group and can take place in our "
            "studio or at your own premises.",
            "Groups of 8 to 20 people\nAdapted to the group's level\n"
            "At the studio or at your offices\nMonthly attendance report\n"
            "Discount on annual agreements",
        ),
    },
]

SPECIALTIES = [
    ("sila", "Сила", "Strength"),
    ("kondicija", "Кондиција", "Conditioning"),
    ("olimpisko-krevanje", "Олимписко кревање", "Olympic lifting"),
    ("mobilnost", "Мобилност", "Mobility"),
    ("joga", "Јога", "Yoga"),
    ("ishrana", "Исхрана", "Nutrition"),
    ("boks", "Бокс", "Boxing"),
    ("rehabilitacija", "Рехабилитација", "Rehabilitation"),
]

TRAINERS = [
    {
        "slug": "marko-stefanovski",
        "name": "Марко Стефановски",
        "name_en": "Marko Stefanovski",
        "years": 12,
        "specialties": ["sila", "olimpisko-krevanje"],
        "email": "marko@forgefitness.mk",
        "mk": (
            "Главен тренер за сила",
            "Дванаесет години искуство во тренинг за сила и поранешен натпреварувач во powerlifting.",
            "Марко го основа FORGE во 2019 година по десет години работа како "
            "тренер во Скопје и Софија. Се натпреварувал во powerlifting на "
            "национално ниво и има посебен интерес за техника на чучањ и мртво "
            "кревање. Работи главно со напредни членови и со луѓе кои се "
            "подготвуваат за натпревар.",
            "NSCA сертифициран тренер за сила и кондиција\nПрва помош и CPR\n"
            "Сертификат за олимписко кревање, второ ниво",
        ),
        "en": (
            "Head strength coach",
            "Twelve years coaching strength, and a former competitive powerlifter.",
            "Marko founded FORGE in 2019 after ten years coaching in Skopje and "
            "Sofia. He competed in powerlifting at national level and has a "
            "particular interest in squat and deadlift technique. He works "
            "mainly with advanced members and people preparing to compete.",
            "NSCA certified strength & conditioning coach\nFirst aid and CPR\n"
            "Olympic weightlifting certificate, level two",
        ),
    },
    {
        "slug": "ana-petrovska",
        "name": "Ана Петровска",
        "name_en": "Ana Petrovska",
        "years": 8,
        "specialties": ["kondicija", "boks"],
        "email": "ana@forgefitness.mk",
        "mk": (
            "Тренер за кондиција",
            "Ги води HIIT и бокс кондиција часовите, со фокус на почетници.",
            "Ана дошла во тренинг преку атлетика, каде се натпреварувала на "
            "средни патеки. Денес ги води најпосетените групни часови во "
            "студиото. Има репутација дека знае да направи тежок тренинг да "
            "изгледа изводлив за некој кој влегува во сала за прв пат.",
            "Сертифициран инструктор за групен фитнес\nБокс кондиција, прво ниво\n"
            "Прва помош и CPR",
        ),
        "en": (
            "Conditioning coach",
            "Leads the HIIT and boxing conditioning classes, with a focus on beginners.",
            "Ana came to coaching through athletics, where she competed over "
            "middle distances. She now runs the busiest group classes in the "
            "studio and has a reputation for making a hard session feel doable "
            "for someone walking into a gym for the first time.",
            "Certified group fitness instructor\nBoxing conditioning, level one\n"
            "First aid and CPR",
        ),
    },
    {
        "slug": "damjan-ilievski",
        "name": "Дамјан Илиевски",
        "name_en": "Damjan Ilievski",
        "years": 15,
        "specialties": ["olimpisko-krevanje", "sila"],
        "email": "damjan@forgefitness.mk",
        "mk": (
            "Тренер за олимписко кревање",
            "Поранешен репрезентативец, работи со техника на потрг и потисок.",
            "Дамјан се натпреварувал петнаесет години и бил дел од националната "
            "репрезентација. Неговите часови се мали по обем бидејќи техниката "
            "на олимписките кревања бара индивидуално внимание. Работи и со "
            "спортисти од други спортови кои сакаат да развијат експлозивност.",
            "Тренер за олимписко кревање, трето ниво\nПоранешен член на национална репрезентација\n"
            "Спортска исхрана, основно ниво",
        ),
        "en": (
            "Olympic lifting coach",
            "A former international lifter, focused on snatch and clean & jerk technique.",
            "Damjan competed for fifteen years and was part of the national "
            "team. His classes are deliberately small, because Olympic lifting "
            "technique needs individual attention. He also works with athletes "
            "from other sports who want to develop explosive power.",
            "Olympic weightlifting coach, level three\nFormer national team member\n"
            "Sports nutrition, foundation level",
        ),
    },
    {
        "slug": "elena-naumova",
        "name": "Елена Наумова",
        "name_en": "Elena Naumova",
        "years": 9,
        "specialties": ["joga", "mobilnost", "rehabilitacija"],
        "email": "elena@forgefitness.mk",
        "mk": (
            "Инструктор за јога и мобилност",
            "Ги води јога и мобилност часовите и работи со членови во рехабилитација.",
            "Елена предава јога девет години и се специјализирала за работа со "
            "луѓе кои кренаат тешко и имаат ограничена подвижност. Нејзините "
            "часови по мобилност се најпосетени од членовите кои тренираат сила "
            "— што е точно она за што се замислени.",
            "Регистриран јога инструктор, 500 часа\nФункционална проценка на движење\n"
            "Работа со лица во рехабилитација",
        ),
        "en": (
            "Yoga & mobility instructor",
            "Runs the yoga and mobility classes and works with members in rehab.",
            "Elena has taught yoga for nine years and specialises in working "
            "with people who lift heavy and have limited range of motion. Her "
            "mobility classes are most popular with the strength members — "
            "which is exactly what they were designed for.",
            "Registered yoga teacher, 500 hours\nFunctional movement assessment\n"
            "Experience working with members in rehabilitation",
        ),
    },
    {
        "slug": "viktor-trajkovski",
        "name": "Виктор Трајковски",
        "name_en": "Viktor Trajkovski",
        "years": 6,
        "specialties": ["sila", "kondicija"],
        "email": "viktor@forgefitness.mk",
        "mk": (
            "Персонален тренер",
            "Работи со почетници и со членови кои се враќаат на тренинг по пауза.",
            "Виктор води најмногу воведни сесии во студиото. Ако никогаш не си "
            "тренирал со тегови или се враќаш по неколку години пауза, "
            "најверојатно првиот тренинг ќе биде со него. Трпелив е и не брза "
            "со оптоварувањата.",
            "Персонален тренер, сертифициран\nФункционален тренинг, второ ниво\nПрва помош и CPR",
        ),
        "en": (
            "Personal trainer",
            "Works with beginners and members returning after a break.",
            "Viktor runs most of the induction sessions in the studio. If you "
            "have never trained with weights, or you are coming back after a few "
            "years away, your first session will probably be with him. He is "
            "patient and does not rush the loading.",
            "Certified personal trainer\nFunctional training, level two\nFirst aid and CPR",
        ),
    },
    {
        "slug": "sara-jovanova",
        "name": "Сара Јованова",
        "name_en": "Sara Jovanova",
        "years": 7,
        "specialties": ["ishrana"],
        "email": "sara@forgefitness.mk",
        "mk": (
            "Нутриционист",
            "Сертифициран нутриционист, ги води советувањата за исхрана.",
            "Сара работи со членови кои сакаат да ослабат, да добијат мускулна "
            "маса или едноставно да јадат подобро без да им го комплицира "
            "животот. Не работи со екстремни диети и не продава суплементи.",
            "Дипломиран нутриционист\nСпортска исхрана, напредно ниво\nРабота со спортисти во подготовка",
        ),
        "en": (
            "Nutritionist",
            "A certified nutritionist who runs the nutrition consultations.",
            "Sara works with members who want to lose fat, gain muscle, or "
            "simply eat better without complicating their lives. She does not "
            "work with extreme diets and does not sell supplements.",
            "Degree in nutrition\nSports nutrition, advanced level\nExperience with athletes in preparation",
        ),
    },
]

ROOMS_EN = {
    "Студио А": "Studio A",
    "Студио Б": "Studio B",
    "Сала за сила": "Strength room",
    "Спининг сала": "Spin room",
    "Функционална зона": "Functional zone",
    "Платформи": "Platforms",
}

CLASSES = [
    {
        "slug": "hiit",
        "trainer": "ana-petrovska",
        "intensity": "high",
        "duration": 45,
        "capacity": 16,
        "mk": (
            "HIIT",
            "Четириесет и пет минути интервали со високо темпо и кратки паузи.",
            "HIIT е најбрзиот начин да ја подигнеш кондицијата ако имаш малку "
            "време. Часот се состои од кратки интервали со максимален интензитет "
            "и контролирани паузи. Секој интервал може да се прилагоди — "
            "почетниците ја намалуваат тежината, не темпото.",
            "Подобрена аеробна и анаеробна кондиција\nВисока потрошувачка на калории\n"
            "Изводливо за секое ниво, со прилагодување\nБез потреба од претходно искуство",
        ),
        "en": (
            "HIIT",
            "Forty-five minutes of high-tempo intervals with short rests.",
            "HIIT is the fastest way to build conditioning if you are short on "
            "time. The class is built from short maximum-intensity intervals "
            "with controlled rest. Every interval can be scaled — beginners "
            "reduce the load, not the tempo.",
            "Improved aerobic and anaerobic conditioning\nHigh calorie expenditure\n"
            "Scalable to any level\nNo previous experience required",
        ),
        "sessions": [(0, time(7, 0), "Студио А"), (0, time(18, 30), "Студио А"),
                     (2, time(7, 0), "Студио А"), (2, time(18, 30), "Студио А"),
                     (4, time(18, 0), "Студио А")],
    },
    {
        "slug": "sila-101",
        "trainer": "viktor-trajkovski",
        "intensity": "medium",
        "duration": 60,
        "capacity": 10,
        "mk": (
            "Сила 101",
            "Воведен час за чучањ, потисок и мртво кревање, за апсолутни почетници.",
            "Ако никогаш не си кревал со шипка, овој час е појдовната точка. "
            "Групата е мала за да може тренерот да ја коригира техниката на "
            "секој поединец. Почнуваме со празна шипка и додаваме тежина само "
            "кога движењето е чисто.",
            "Правилна техника на трите основни кревања\nМала група, најмногу десет луѓе\n"
            "Индивидуална корекција на техника\nЈасен план за напредување",
        ),
        "en": (
            "Strength 101",
            "An introductory class covering the squat, press and deadlift for complete beginners.",
            "If you have never lifted with a barbell, this is the starting "
            "point. The group is kept small so the coach can correct each "
            "person individually. We start with an empty bar and add weight "
            "only once the movement is clean.",
            "Correct technique in the three main lifts\nSmall group, ten people maximum\n"
            "Individual technique correction\nA clear plan for progressing",
        ),
        "sessions": [(1, time(18, 0), "Сала за сила"), (3, time(18, 0), "Сала за сила"),
                     (5, time(10, 0), "Сала за сила")],
    },
    {
        "slug": "spining",
        "trainer": "ana-petrovska",
        "intensity": "high",
        "duration": 50,
        "capacity": 20,
        "mk": (
            "Спининг",
            "Кардио на велосипед со музика и структурирани интервали.",
            "Педесет минути на велосипед, со профил на отпор кој се менува низ "
            "часот. Отпорот го поставуваш самиот, така што истиот час "
            "функционира и за некој што почнува и за некој што трча маратон.",
            "Одличен кардио тренинг без оптоварување на зглобовите\n"
            "Самостојно поставување на отпорот\nПогодно за опоравување помеѓу тешки тренинзи",
        ),
        "en": (
            "Spin",
            "Bike cardio with music and structured intervals.",
            "Fifty minutes on the bike with a resistance profile that changes "
            "through the class. You set the resistance yourself, so the same "
            "class works for someone starting out and someone running marathons.",
            "Excellent cardio with no joint impact\nYou control your own resistance\n"
            "Good for recovery between heavy sessions",
        ),
        "sessions": [(1, time(7, 0), "Спининг сала"), (1, time(19, 0), "Спининг сала"),
                     (3, time(7, 0), "Спининг сала"), (5, time(9, 0), "Спининг сала")],
    },
    {
        "slug": "joga-flou",
        "trainer": "elena-naumova",
        "intensity": "low",
        "duration": 60,
        "capacity": 18,
        "mk": (
            "Јога Флоу",
            "Динамична јога со фокус на дишење, рамнотежа и подвижност.",
            "Часот се движи низ поврзана низа од пози, со внимание на дишењето. "
            "Не е потребно претходно искуство и не е потребна екстремна "
            "флексибилност — секоја поза има полесна варијанта.",
            "Подобрена подвижност и рамнотежа\nНамалување на напнатост во грбот и рамената\n"
            "Полесни варијанти за секоја поза\nОдлична дополна на тренинг за сила",
        ),
        "en": (
            "Yoga Flow",
            "Dynamic yoga focused on breath, balance and mobility.",
            "The class moves through a linked sequence of poses with attention "
            "to the breath. No previous experience is needed and no extreme "
            "flexibility either — every pose has an easier variation.",
            "Improved mobility and balance\nReduced tension in the back and shoulders\n"
            "Easier variations for every pose\nAn excellent complement to strength training",
        ),
        "sessions": [(1, time(20, 0), "Студио Б"), (3, time(20, 0), "Студио Б"),
                     (6, time(10, 0), "Студио Б")],
    },
    {
        "slug": "boks-kondicija",
        "trainer": "ana-petrovska",
        "intensity": "high",
        "duration": 55,
        "capacity": 14,
        "mk": (
            "Бокс кондиција",
            "Боксерска техника и кондиција, без контакт и без спаринг.",
            "Учиш основни удари и движење на нозете, а потоа ги применуваш на "
            "вреќа и на фокусери. Нема контакт помеѓу учесниците. Часот е "
            "интензивен и одличен за координација.",
            "Основна боксерска техника\nСилен кардио тренинг\nПодобрена координација\n"
            "Без контакт и без спаринг\nРакавици обезбедува студиото",
        ),
        "en": (
            "Boxing conditioning",
            "Boxing technique and conditioning, with no contact and no sparring.",
            "You learn basic punches and footwork, then apply them on the bag "
            "and on pads. There is no contact between participants. The class "
            "is intense and excellent for coordination.",
            "Fundamental boxing technique\nStrong cardio workout\nImproved coordination\n"
            "No contact and no sparring\nGloves provided by the studio",
        ),
        "sessions": [(0, time(20, 0), "Студио А"), (2, time(20, 0), "Студио А"),
                     (4, time(19, 0), "Студио А")],
    },
    {
        "slug": "funkcionalen-trening",
        "trainer": "viktor-trajkovski",
        "intensity": "medium",
        "duration": 50,
        "capacity": 14,
        "mk": (
            "Функционален тренинг",
            "Движења од секојдневниот живот, изведени под контролирано оптоварување.",
            "Работиме со сопствена тежина, ѕвона, јажиња и санки. Целта е сила "
            "која се пренесува надвор од салата — носење, кревање од под, "
            "качување скали без задишување.",
            "Сила која се пренесува во секојдневието\nРазновидни движења, без монотонија\n"
            "Прилагодливо за секое ниво\nПодобрена стабилност на трупот",
        ),
        "en": (
            "Functional training",
            "Everyday movement patterns performed under controlled load.",
            "We work with bodyweight, kettlebells, ropes and sleds. The aim is "
            "strength that transfers outside the gym — carrying, lifting from "
            "the floor, climbing stairs without getting out of breath.",
            "Strength that transfers to daily life\nVaried movements, never monotonous\n"
            "Scalable to any level\nImproved trunk stability",
        ),
        "sessions": [(1, time(12, 0), "Функционална зона"), (3, time(12, 0), "Функционална зона"),
                     (5, time(11, 0), "Функционална зона")],
    },
    {
        "slug": "mobilnost",
        "trainer": "elena-naumova",
        "intensity": "low",
        "duration": 40,
        "capacity": 16,
        "mk": (
            "Мобилност",
            "Четириесет минути насочени кон подвижност на колковите, рамената и 'рбетот.",
            "Кратка сесија замислена како дополнение на тренингот за сила. Ако "
            "чучаш длабоко со тешкотија или те боли рамото при потисок над "
            "глава, овој час директно ги адресира тие ограничувања.",
            "Поголем опсег на движење во чучањ и потисок\nНамалена вкочанетост по седење\n"
            "Вежби што можеш да ги правиш дома\nИдеално пред тежок тренинг",
        ),
        "en": (
            "Mobility",
            "Forty minutes targeting hip, shoulder and spine range of motion.",
            "A short session designed as a complement to strength training. If "
            "you struggle to squat deep, or your shoulder hurts pressing "
            "overhead, this class addresses those restrictions directly.",
            "Greater range in the squat and press\nLess stiffness after sitting all day\n"
            "Exercises you can repeat at home\nIdeal before a heavy session",
        ),
        "sessions": [(0, time(12, 0), "Студио Б"), (2, time(12, 0), "Студио Б"),
                     (4, time(17, 0), "Студио Б"), (6, time(11, 30), "Студио Б")],
    },
    {
        "slug": "olimpisko-krevanje",
        "trainer": "damjan-ilievski",
        "intensity": "high",
        "duration": 75,
        "capacity": 8,
        "mk": (
            "Олимписко кревање",
            "Потрг и потисок, во мала група со индивидуално внимание.",
            "Најтехничкиот час во студиото. Групата е ограничена на осум луѓе "
            "затоа што овие кревања бараат постојана корекција. Работиме "
            "постепено — прво позиции, потоа делови од движењето, па целото "
            "кревање.",
            "Техника на потрг и потисок\nМала група, најмногу осум луѓе\n"
            "Постојана индивидуална корекција\nРазвој на експлозивна сила\n"
            "Погодно и за спортисти од други спортови",
        ),
        "en": (
            "Olympic lifting",
            "Snatch and clean & jerk, in a small group with individual attention.",
            "The most technical class in the studio. The group is capped at "
            "eight because these lifts need constant correction. We build up "
            "gradually — positions first, then parts of the movement, then the "
            "full lift.",
            "Snatch and clean & jerk technique\nSmall group, eight people maximum\n"
            "Constant individual correction\nDevelops explosive power\n"
            "Also suitable for athletes from other sports",
        ),
        "sessions": [(1, time(17, 0), "Платформи"), (3, time(17, 0), "Платформи"),
                     (5, time(12, 0), "Платформи")],
    },
]

PLANS = [
    {
        "slug": "osnoven",
        "price": 1500,
        "featured": False,
        "mk": ("Основен", "За членови кои тренираат самостојно.", "месечно",
               "Неограничен пристап до салата\nПристап во сите работни часови\n"
               "Гардероба и туш\nБесплатна воведна сесија\nБез договор за обврзување"),
        "en": ("Basic", "For members who train on their own.", "per month",
               "Unlimited gym floor access\nAccess during all opening hours\n"
               "Locker and shower\nFree induction session\nNo lock-in contract"),
    },
    {
        "slug": "celosen",
        "price": 2400,
        "featured": True,
        "mk": ("Целосен", "Најпопуларен — сала плус сите групни часови.", "месечно",
               "Сè од Основен\nНеограничени групни часови\nПриоритетна резервација\n"
               "Фитнес проценка на 12 недели\nЗамрзнување до 2 месеци\nЕден гостин месечно"),
        "en": ("Full", "Most popular — the floor plus every group class.", "per month",
               "Everything in Basic\nUnlimited group classes\nPriority class booking\n"
               "Fitness assessment every 12 weeks\nFreeze for up to 2 months\nOne guest pass a month"),
    },
    {
        "slug": "premium",
        "price": 3900,
        "featured": False,
        "mk": ("Премиум", "Со персонален тренинг и нутриционистичка поддршка.", "месечно",
               "Сè од Целосен\nЧетири персонални тренинзи месечно\n"
               "Нутриционистичко советување\nИндивидуална програма за сила\n"
               "Еден третман спортска масажа месечно\nНеограничени гостински влезови"),
        "en": ("Premium", "With personal training and nutrition support.", "per month",
               "Everything in Full\nFour personal training sessions a month\n"
               "Nutrition consultation\nIndividual strength programme\n"
               "One sports massage a month\nUnlimited guest passes"),
    },
]

BLOG_CATEGORIES = [
    ("trening", "Тренинг", "Training", 1),
    ("ishrana", "Исхрана", "Nutrition", 2),
    ("oporavuvanje", "Опоравување", "Recovery", 3),
    ("novosti", "Новости", "News", 4),
]

POSTS = [
    {
        "slug": "kolku-cesto-treba-da-treniras",
        "cat": "trening",
        "author": "marko-stefanovski",
        "days_ago": 3,
        "mk": (
            "Колку често треба да тренираш?",
            "Три пати неделно е доволно за поголемиот дел од луѓето — под услов тие три тренинзи да се доследни.",
            "Најчестото прашање што го добиваме е колку пати неделно треба да се "
            "тренира. Одговорот е поедноставен отколку што повеќето очекуваат.\n\n"
            "За некој што почнува, три тренинзи неделно се сосема доволни. "
            "Истражувањата постојано покажуваат дека разликата помеѓу три и пет "
            "тренинзи неделно е мала кај почетниците, а ризикот од откажување е "
            "многу поголем кога планот е преамбициозен.\n\n"
            "Поважно од бројот е доследноста. Три тренинзи неделно во текот на "
            "шест месеци даваат далеку подобри резултати од шест тренинзи неделно "
            "во текот на три недели, проследени со откажување.\n\n"
            "Ако веќе тренираш една или две години и напредокот застанал, тогаш "
            "четири до пет тренинзи има смисла. Но тоа е проблем што доаѓа "
            "подоцна, не на почеток.\n\n"
            "Нашиот совет: избери број што сигурно можеш да го одржиш и држи се "
            "до него три месеци пред да размислуваш за зголемување.",
        ),
        "en": (
            "How often should you actually train?",
            "Three times a week is enough for most people — provided those three sessions are consistent.",
            "The most common question we get is how many times a week someone "
            "should train. The answer is simpler than most people expect.\n\n"
            "For someone starting out, three sessions a week is plenty. Research "
            "consistently shows the difference between three and five sessions a "
            "week is small for beginners, while the risk of quitting is far "
            "higher when the plan is over-ambitious.\n\n"
            "Consistency matters more than frequency. Three sessions a week for "
            "six months produces far better results than six sessions a week for "
            "three weeks followed by giving up.\n\n"
            "If you have been training for a year or two and progress has "
            "stalled, four or five sessions starts to make sense. But that is a "
            "problem for later, not for the beginning.\n\n"
            "Our advice: pick a number you can definitely sustain and hold it "
            "for three months before thinking about increasing it.",
        ),
    },
    {
        "slug": "proteini-kolku-navistina-ti-trebaat",
        "cat": "ishrana",
        "author": "sara-jovanova",
        "days_ago": 9,
        "mk": (
            "Протеини: колку навистина ти требаат?",
            "Помеѓу 1,6 и 2,2 грама по килограм телесна тежина. Сè над тоа е потрошени пари.",
            "Индустријата за суплементи има интерес да мислиш дека ти требаат "
            "огромни количини протеин. Бројките велат нешто друго.\n\n"
            "За луѓе кои тренираат со отпор, литературата прилично доследно "
            "покажува дека внесот помеѓу 1,6 и 2,2 грама по килограм телесна "
            "тежина дневно е доволен за максимален раст на мускулна маса. За "
            "човек од 75 килограми тоа е околу 120 до 165 грама дневно.\n\n"
            "Сè над таа граница не носи дополнителна корист. Телото едноставно "
            "го користи вишокот како извор на енергија, што е скап начин да се "
            "внесат калории.\n\n"
            "Второ што вреди да се знае: распоредот низ денот е помалку важен "
            "отколку што се мислеше. Не постои 'анаболен прозорец' од триесет "
            "минути по тренингот. Вкупниот дневен внес е она што има значење.\n\n"
            "Најдобриот извор е обична храна — јајца, месо, риба, млечни "
            "производи, мешунки. Протеинскиот прав е практичен, но не е "
            "неопходен.",
        ),
        "en": (
            "Protein: how much do you actually need?",
            "Between 1.6 and 2.2 grams per kilogram of bodyweight. Anything above that is money wasted.",
            "The supplement industry has an interest in you believing you need "
            "enormous amounts of protein. The numbers say otherwise.\n\n"
            "For people doing resistance training, the literature fairly "
            "consistently shows an intake between 1.6 and 2.2 grams per kilogram "
            "of bodyweight per day is enough for maximal muscle growth. For a "
            "75 kilogram person that is roughly 120 to 165 grams a day.\n\n"
            "Anything beyond that provides no further benefit. The body simply "
            "uses the excess as an energy source, which is an expensive way to "
            "get calories.\n\n"
            "The second thing worth knowing: timing through the day matters less "
            "than was once thought. There is no thirty-minute anabolic window "
            "after training. Total daily intake is what counts.\n\n"
            "The best source is ordinary food — eggs, meat, fish, dairy, "
            "legumes. Protein powder is convenient, but it is not necessary.",
        ),
    },
    {
        "slug": "zoshto-son-e-najvazen-za-oporavuvanje",
        "cat": "oporavuvanje",
        "author": "elena-naumova",
        "days_ago": 16,
        "mk": (
            "Зошто сонот е најважниот дел од опоравувањето",
            "Ниту еден суплемент не може да го замени она што го прават седум до девет часа сон.",
            "Ако тренираш редовно но постојано си уморен и не напредуваш, првото "
            "место каде треба да погледнеш не е програмата — туку сонот.\n\n"
            "За време на длабок сон телото ослободува најголем дел од хормонот "
            "за раст, поправа мускулно ткиво и ги обновува залихите на гликоген. "
            "Кратењето на сонот на пет или шест часа мерливо ја намалува силата, "
            "ја забавува реакцијата и го зголемува чувството на напор при иста "
            "тежина.\n\n"
            "Практично, три работи прават најголема разлика:\n\n"
            "Прво, доследно време на легнување. Телото реагира подобро на "
            "редовност отколку на вкупен број часови.\n\n"
            "Второ, температура на просторијата. Околу 18 степени е оптимално за "
            "повеќето луѓе.\n\n"
            "Трето, кофеин. Полуживотот на кофеинот е околу пет до шест часа, "
            "што значи дека кафето во четири попладне сè уште дејствува кога "
            "легнуваш.\n\n"
            "Ако можеш да избереш само една промена за подобри резултати, "
            "изберете ја оваа.",
        ),
        "en": (
            "Why sleep is the most important part of recovery",
            "No supplement replaces what seven to nine hours of sleep does for you.",
            "If you train regularly but feel permanently tired and are not "
            "progressing, the first place to look is not your programme — it is "
            "your sleep.\n\n"
            "During deep sleep the body releases most of its growth hormone, "
            "repairs muscle tissue and restores glycogen stores. Cutting sleep to "
            "five or six hours measurably reduces strength, slows reaction time "
            "and increases perceived effort at the same load.\n\n"
            "In practice, three things make the biggest difference.\n\n"
            "First, a consistent bedtime. The body responds better to regularity "
            "than to total hours.\n\n"
            "Second, room temperature. Around 18 degrees suits most people.\n\n"
            "Third, caffeine. Its half-life is roughly five to six hours, which "
            "means a coffee at four in the afternoon is still working when you go "
            "to bed.\n\n"
            "If you can only change one thing to get better results, make it "
            "this one.",
        ),
    },
    {
        "slug": "pet-najchesti-greshki-vo-chuchanj",
        "cat": "trening",
        "author": "marko-stefanovski",
        "days_ago": 23,
        "mk": (
            "Пет најчести грешки во чучањ",
            "Колената што паѓаат навнатре се симптом, не причина. Еве што навистина да поправиш.",
            "Чучањот е движење што сите го изведуваат и малкумина го изведуваат "
            "добро. Овие пет грешки ги гледаме секој ден.\n\n"
            "Прва: премногу тежина преруно. Ако техниката се распаѓа во "
            "последните повторувања, тежината е преголема — без исклучок.\n\n"
            "Втора: колената паѓаат навнатре. Ова обично не е проблем со "
            "колената туку со силата на глутеусите или со позицијата на стапалата. "
            "Обиди се да ги 'завртиш' стапалата во подот без да ги мрдаш.\n\n"
            "Трета: подигнување на петиците. Речиси секогаш е ограничена "
            "подвижност на глуждот. Часот по мобилност директно го адресира ова.\n\n"
            "Четврта: заоблување на долниот дел од грбот на дното. Спушти се "
            "само толку длабоко колку што можеш да ја задржиш неутралната "
            "позиција, па постепено работи на длабочината.\n\n"
            "Петта: задржување на здивот низ целото повторување. Земи здив на "
            "врвот, задржи низ спуштањето, издиши на излегување.\n\n"
            "Ако не си сигурен што од ова се однесува на тебе, дојди на час "
            "Сила 101 и ќе поминеме низ твојата техника.",
        ),
        "en": (
            "Five common squat mistakes",
            "Knees caving in is a symptom, not a cause. Here is what to actually fix.",
            "The squat is a movement everybody performs and few perform well. "
            "These five mistakes we see every day.\n\n"
            "One: too much weight too soon. If technique falls apart on the last "
            "reps, the weight is too heavy — without exception.\n\n"
            "Two: knees caving inward. This is usually not a knee problem but a "
            "glute strength or foot position problem. Try to 'screw' your feet "
            "into the floor without actually moving them.\n\n"
            "Three: heels lifting. Almost always restricted ankle mobility. The "
            "mobility class addresses this directly.\n\n"
            "Four: lower back rounding at the bottom. Only descend as far as you "
            "can hold a neutral position, then work on depth gradually.\n\n"
            "Five: holding your breath through the whole rep. Take a breath at "
            "the top, hold it through the descent, exhale on the way up.\n\n"
            "If you are not sure which of these applies to you, come to a "
            "Strength 101 class and we will go through your technique.",
        ),
    },
    {
        "slug": "novo-studio-b-i-prosiruvanje",
        "cat": "novosti",
        "author": "marko-stefanovski",
        "days_ago": 34,
        "mk": (
            "Отворивме Студио Б и додадовме нови часови",
            "Дополнителни 180 квадрати за јога, мобилност и функционален тренинг.",
            "Од овој месец Студио Б е отворено за членови. Просторот е наменет "
            "за часовите по јога и мобилност кои досега се одржуваа во главната "
            "сала и често беа претесни.\n\n"
            "Новиот простор има подно греење, огледала на две страни и целосна "
            "опрема за мобилност — валјаци, ленти, блокови и душеци за секој "
            "учесник.\n\n"
            "Со отворањето додадовме и четири нови термини неделно: два за "
            "мобилност во попладневните часови и два за јога наутро. Целосниот "
            "распоред е достапен на страницата со неделен распоред.\n\n"
            "Резервациите за новите термини се отворени за сите членови со "
            "Целосен и Премиум пакет.",
        ),
        "en": (
            "Studio B is open and we've added new classes",
            "An extra 180 square metres for yoga, mobility and functional training.",
            "From this month Studio B is open to members. The space is intended "
            "for the yoga and mobility classes that until now ran in the main "
            "hall and were frequently too cramped.\n\n"
            "The new space has underfloor heating, mirrors on two walls and a "
            "full set of mobility equipment — rollers, bands, blocks and a mat "
            "for every participant.\n\n"
            "Alongside the opening we have added four new slots a week: two "
            "mobility sessions in the afternoon and two yoga classes in the "
            "morning. The full timetable is on the weekly schedule page.\n\n"
            "Bookings for the new slots are open to all members on the Full and "
            "Premium plans.",
        ),
    },
    {
        "slug": "kako-da-se-vratis-na-trening-po-pauza",
        "cat": "trening",
        "author": "viktor-trajkovski",
        "days_ago": 45,
        "mk": (
            "Како да се вратиш на тренинг по долга пауза",
            "Најголемата грешка е да продолжиш таму каде што застана. Почни на педесет отсто.",
            "Враќањето по пауза од неколку месеци или години е ситуација што ја "
            "гледаме постојано. Речиси секогаш истата грешка се повторува.\n\n"
            "Луѓето се обидуваат да продолжат со тежините што ги кревале порано. "
            "Мускулната меморија е реална и силата се враќа побрзо отколку што "
            "била изградена — но сврзното ткиво, тетивите и лигаментите се "
            "адаптираат многу побавно од мускулите. Токму затоа повредите при "
            "враќање се толку чести.\n\n"
            "Практичниот пристап: почни со педесет до шеесет отсто од тежините "
            "што си ги кревал последен пат. Прв месец работи со тежини што ти "
            "изгледаат прелесни. Ако по тренинг не си воопшто болен, тоа е "
            "добар знак, не лош.\n\n"
            "Втор месец додај дваесет отсто. Трет месец обично си блиску до "
            "претходното ниво, но со здрави зглобови.\n\n"
            "Три месеци трпение наспроти три месеци рехабилитација — изборот е "
            "прилично јасен.",
        ),
        "en": (
            "How to return to training after a long break",
            "The biggest mistake is picking up where you left off. Start at fifty percent.",
            "Coming back after a break of months or years is a situation we see "
            "constantly, and nearly always with the same mistake.\n\n"
            "People try to continue with the weights they used before. Muscle "
            "memory is real and strength returns faster than it was built — but "
            "connective tissue, tendons and ligaments adapt far more slowly than "
            "muscle. That is precisely why comeback injuries are so common.\n\n"
            "The practical approach: start at fifty to sixty percent of the "
            "weights you last handled. For the first month work with loads that "
            "feel too easy. If you are not sore after a session, that is a good "
            "sign, not a bad one.\n\n"
            "In the second month add twenty percent. By the third month you are "
            "usually close to your previous level, but with healthy joints.\n\n"
            "Three months of patience against three months of rehab — the choice "
            "is fairly clear.",
        ),
    },
    {
        "slug": "shto-da-jades-pred-i-po-trening",
        "cat": "ishrana",
        "author": "sara-jovanova",
        "days_ago": 58,
        "mk": (
            "Што да јадеш пред и по тренинг",
            "Едноставни правила без комплицирање: јаглехидрати пред, протеини и јаглехидрати потоа.",
            "Прашањето за оброците околу тренингот носи многу непотребна "
            "комплексност. Основите се едноставни.\n\n"
            "Пред тренинг, целта е да имаш достапна енергија без да ти биде "
            "тешко. Оброк со јаглехидрати и малку протеин, два до три часа пред "
            "тренинг, функционира за повеќето луѓе. Ако тренираш наутро и не "
            "можеш да јадеш, банана триесет минути порано е доволна.\n\n"
            "Избегнувај многу масти и многу влакна непосредно пред тренинг — "
            "забавуваат празнење на желудникот и предизвикуваат непријатност.\n\n"
            "По тренинг, комбинација од протеин и јаглехидрати помага во "
            "опоравувањето. Но, како што пишувавме порано, нема потреба од "
            "паника околу времето. Ако јадеш нормален оброк во рок од неколку "
            "часа, тоа е сосема доволно.\n\n"
            "Хидратацијата е почесто занемарена од исхраната. Ако си жеден за "
            "време на тренинг, веќе доцниш.",
        ),
        "en": (
            "What to eat before and after training",
            "Simple rules without the complication: carbs before, protein and carbs after.",
            "The question of meals around training carries a lot of unnecessary "
            "complexity. The basics are simple.\n\n"
            "Before training, the aim is available energy without feeling heavy. "
            "A meal with carbohydrates and some protein, two to three hours "
            "beforehand, works for most people. If you train in the morning and "
            "cannot eat, a banana thirty minutes earlier is enough.\n\n"
            "Avoid a lot of fat and a lot of fibre immediately before training — "
            "they slow gastric emptying and cause discomfort.\n\n"
            "After training, a combination of protein and carbohydrate helps "
            "recovery. But as we wrote previously, there is no need to panic "
            "about timing. Eating a normal meal within a few hours is entirely "
            "sufficient.\n\n"
            "Hydration is neglected more often than nutrition. If you are "
            "thirsty during a session, you are already behind.",
        ),
    },
    {
        "slug": "bolka-vo-ramo-pri-potisok",
        "cat": "oporavuvanje",
        "author": "elena-naumova",
        "days_ago": 71,
        "mk": (
            "Болка во рамото при потисок над глава",
            "Најчесто не е проблем во самото рамо, туку во подвижноста на градниот дел од 'рбетот.",
            "Болката во рамото при потисок над глава е една од најчестите "
            "поплаки кај луѓе што кренат. Инстинктивната реакција е да се "
            "работи на рамото — но причината често е на друго место.\n\n"
            "За да ја подигнеш шипката право над главата, потребна е екстензија "
            "во градниот дел од 'рбетот. Ако тој дел е вкочанет, а тоа е речиси "
            "универзално кај луѓе што седат осум часа дневно, рамото мора да "
            "компензира со дополнителна ротација. Таа компензација е она што "
            "боли.\n\n"
            "Пробај едноставен тест: седни на под со грб до ѕид и обиди се да ги "
            "подигнеш рацете право нагоре, држејќи го долниот дел од грбот "
            "прилепен. Ако рацете не стигаат до ѕидот, ограничувањето не е во "
            "рамото.\n\n"
            "Работата на подвижноста на градниот 'рбет обично дава подобрување "
            "во рок од неколку недели. Ако болката е остра, се шири надолу по "
            "раката или се јавува и во мирување, тогаш е потребен преглед кај "
            "физиотерапевт пред да продолжиш со тренинг.",
        ),
        "en": (
            "Shoulder pain when pressing overhead",
            "Usually it is not the shoulder itself but thoracic spine mobility.",
            "Shoulder pain when pressing overhead is one of the most common "
            "complaints among people who lift. The instinctive response is to "
            "work on the shoulder — but the cause is often elsewhere.\n\n"
            "To press a bar directly overhead you need extension through the "
            "thoracic spine. If that region is stiff, which is close to "
            "universal in people who sit eight hours a day, the shoulder has to "
            "compensate with extra rotation. That compensation is what hurts.\n\n"
            "Try a simple test: sit on the floor with your back against a wall "
            "and try to raise your arms straight overhead while keeping your "
            "lower back flat. If your arms cannot reach the wall, the "
            "restriction is not in your shoulder.\n\n"
            "Working on thoracic mobility usually produces improvement within a "
            "few weeks. If the pain is sharp, radiates down the arm or is "
            "present at rest, see a physiotherapist before continuing to train.",
        ),
    },
]

TESTIMONIALS = [
    {
        "author": "Ивана Ристеска",
        "author_en": "Ivana Risteska",
        "rating": 5,
        "featured": True,
        "order": 1,
        "mk": ("Член од 2021",
               "Никогаш не сум влегувала во сала пред FORGE. Виктор ме водеше низ "
               "првите три месеци без ниту еднаш да ме натера да се чувствувам "
               "непријатно. Сега кревам двојно повеќе отколку што мислев дека е можно."),
        "en": ("Member since 2021",
               "I had never set foot in a gym before FORGE. Viktor walked me "
               "through the first three months without once making me feel out of "
               "place. I now lift twice what I thought was possible."),
    },
    {
        "author": "Стефан Ангеловски",
        "author_en": "Stefan Angelovski",
        "rating": 5,
        "featured": True,
        "order": 2,
        "mk": ("Член од 2020",
               "Разликата е во тоа што тука навистина имаш програма. Не доаѓаш и "
               "не се прашуваш што да работиш. Марко ја менува програмата на секои "
               "четири недели и напредокот е мерлив."),
        "en": ("Member since 2020",
               "The difference is that here you genuinely have a programme. You "
               "don't turn up and wonder what to do. Marko adjusts it every four "
               "weeks and the progress is measurable."),
    },
    {
        "author": "Марија Костова",
        "author_en": "Marija Kostova",
        "rating": 5,
        "featured": True,
        "order": 3,
        "mk": ("Член од 2022",
               "Часовите по мобилност на Елена ми ја решија болката во грбот што "
               "ја имав со години од седење пред компјутер. Само тоа вреди повеќе "
               "од цената на членството."),
        "en": ("Member since 2022",
               "Elena's mobility classes fixed the back pain I'd had for years "
               "from sitting at a desk. That alone is worth more than the price of "
               "the membership."),
    },
    {
        "author": "Дарко Николовски",
        "author_en": "Darko Nikolovski",
        "rating": 5,
        "featured": False,
        "order": 4,
        "mk": ("Член од 2019",
               "Тренирам тука од отворањето. Салата порасна, но чувството остана "
               "исто — сите те знаат по име и никој не те гледа накриво ако кренеш "
               "полесна тежина."),
        "en": ("Member since 2019",
               "I've trained here since they opened. The place has grown but the "
               "feel hasn't changed — everyone knows your name and nobody looks at "
               "you sideways for lifting lighter."),
    },
    {
        "author": "Ана Здравковска",
        "author_en": "Ana Zdravkovska",
        "rating": 4,
        "featured": False,
        "order": 5,
        "mk": ("Член од 2023",
               "Одлични тренери и чиста опрема. Единствената забелешка е дека "
               "вечерните термини се пополнуваат брзо, па резервацијата е "
               "задолжителна."),
        "en": ("Member since 2023",
               "Excellent coaches and clean equipment. My only note is that "
               "evening slots fill up fast, so booking ahead is essential."),
    },
    {
        "author": "Филип Митревски",
        "author_en": "Filip Mitrevski",
        "rating": 5,
        "featured": False,
        "order": 6,
        "mk": ("Член од 2022",
               "Дојдов по повреда на колено и се плашев дека нема да можам да "
               "чучам повторно. Постепената програма ме врати на целосно "
               "оптоварување за пет месеци."),
        "en": ("Member since 2022",
               "I came in after a knee injury, afraid I'd never squat again. The "
               "graded programme had me back to full loading in five months."),
    },
]

FAQS = [
    ("general", 1,
     ("Дали треба да резервирам за групен час?",
      "Да, за групните часови резервацијата е задолжителна бидејќи бројот на "
      "места е ограничен. Резервација правиш преку рецепција или со телефонски "
      "повик. Вечерните термини се пополнуваат најбрзо."),
     ("Do I need to book for a group class?",
      "Yes — group classes have limited places, so booking is required. You can "
      "book at reception or by phone. Evening slots fill up fastest.")),
    ("general", 2,
     ("Што треба да понесам на првиот тренинг?",
      "Спортска облека, патики за внатре, шише вода и пешкир. Ракавици за бокс "
      "обезбедува студиото. Гардеробите имаат ормарчиња со клуч."),
     ("What should I bring to my first session?",
      "Training clothes, indoor shoes, a water bottle and a towel. Boxing gloves "
      "are provided by the studio. The changing rooms have lockable lockers.")),
    ("general", 3,
     ("Дали има паркинг?",
      "Да, имаме бесплатен паркинг за членови зад зградата, со дваесет и пет "
      "места. Влезот е од страничната улица."),
     ("Is there parking?",
      "Yes — free member parking behind the building with twenty-five spaces. "
      "The entrance is from the side street.")),
    ("membership", 1,
     ("Дали има договор за обврзување?",
      "Нема. Сите пакети се на месечна основа и можат да се откажат со "
      "известување триесет дена однапред. Нема ни трошок за зачленување."),
     ("Is there a lock-in contract?",
      "No. All plans are monthly and can be cancelled with thirty days' notice. "
      "There is no joining fee either.")),
    ("membership", 2,
     ("Може ли да го замрзнам членството?",
      "Да, членовите со Целосен и Премиум пакет можат да замрзнат до два месеци "
      "годишно, на пример поради патување или повреда. Замрзнувањето се "
      "пријавува најдоцна пет дена пред почетокот на месецот."),
     ("Can I freeze my membership?",
      "Yes — Full and Premium members can freeze for up to two months a year, "
      "for example for travel or injury. Freezes must be requested at least five "
      "days before the start of the month.")),
    ("membership", 3,
     ("Може ли да пробам пред да се зачленам?",
      "Секако. Првата сесија е бесплатна и вклучува обиколка на студиото, "
      "кратка проценка и целосен тренинг со тренер. Не бараме податоци за "
      "картичка."),
     ("Can I try before joining?",
      "Of course. Your first session is free and includes a tour of the studio, "
      "a short assessment and a full session with a coach. We don't ask for card "
      "details.")),
    ("membership", 4,
     ("Дали има попуст за студенти?",
      "Да, студентите добиваат петнаесет отсто попуст на сите пакети со важечки "
      "индекс или студентска картичка."),
     ("Is there a student discount?",
      "Yes — students get fifteen percent off all plans with a valid student "
      "card.")),
    ("training", 1,
     ("Никогаш не сум тренирал. Дали часовите се претешки за мене?",
      "Не. Секој час има прилагодени варијанти и тренерите очекуваат почетници. "
      "Ако сакаш да почнеш најблаго, часот Сила 101 е замислен точно за луѓе "
      "кои никогаш не кренале со шипка."),
     ("I've never trained before. Are the classes too hard for me?",
      "No. Every class has scaled variations and the coaches expect beginners. "
      "If you want the gentlest start, Strength 101 is designed precisely for "
      "people who have never touched a barbell.")),
    ("training", 2,
     ("Колку луѓе има на еден групен час?",
      "Зависи од часот. Сила 101 е ограничен на десет луѓе, Олимписко кревање на "
      "осум, а HIIT и спининг примаат до дваесет. Бројот е наведен на страницата "
      "на секој час."),
     ("How many people are in a group class?",
      "It depends on the class. Strength 101 is capped at ten, Olympic lifting at "
      "eight, while HIIT and spin take up to twenty. The number is listed on each "
      "class page.")),
    ("training", 3,
     ("Дали работите со луѓе во рехабилитација по повреда?",
      "Да. Имаме програма за постепено враќање на тренинг што ја правиме во "
      "соработка со физиотерапевт. Потребно е да донесеш наод од твојот лекар "
      "или физиотерапевт пред да почнеме."),
     ("Do you work with people rehabilitating after injury?",
      "Yes. We run a graded return-to-training programme in cooperation with a "
      "physiotherapist. You'll need to bring a report from your doctor or "
      "physiotherapist before we start.")),
]


class Command(BaseCommand):
    help = "Populate the database with realistic bilingual demo content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing content before seeding (does not touch users).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing content…")
            for model in (
                ClassSession, GymClass, MembershipPlan, Post, Category,
                Service, ServiceCategory, TeamMember, Specialty,
                Testimonial, FAQ, OpeningHours,
            ):
                model.objects.all().delete()

        self._site()
        self._hours()
        self._services()
        specialties = self._specialties()
        trainers = self._trainers(specialties)
        self._classes(trainers)
        self._plans()
        self._blog(trainers)
        self._testimonials()
        self._faqs()
        self._images()

        self.stdout.write(self.style.SUCCESS("\nSeed complete."))
        self.stdout.write(
            "Photos are placeholders from seed_assets/ — see seed_assets/CREDITS.md.\n"
            "Create a login with:  python manage.py createsuperuser"
        )


    def _site(self):
        site = SiteSettings.load()
        for field, value in SITE.items():
            setattr(site, field, value)
        site.tagline = SITE["tagline_mk"]
        site.short_about = SITE["short_about_mk"]
        site.street = SITE["street_mk"]
        site.city = SITE["city_mk"]
        site.save()
        self.stdout.write("  site settings")

    def _hours(self):
        for weekday, opens, closes, closed in HOURS:
            OpeningHours.objects.update_or_create(
                weekday=weekday,
                defaults={"opens": opens, "closes": closes, "is_closed": closed},
            )
        self.stdout.write(f"  {len(HOURS)} opening hours")

    def _services(self):
        cats = {}
        for slug, mk, en, order in SERVICE_CATEGORIES:
            cat, _ = ServiceCategory.objects.update_or_create(
                slug=slug,
                defaults={"name": mk, "name_mk": mk, "name_en": en, "order": order},
            )
            cats[slug] = cat

        for i, s in enumerate(SERVICES):
            mk_title, mk_short, mk_full, mk_incl = s["mk"]
            en_title, en_short, en_full, en_incl = s["en"]
            Service.objects.update_or_create(
                slug=s["slug"],
                defaults={
                    "category": cats[s["cat"]],
                    "icon": s["icon"],
                    "is_featured": s["featured"],
                    "price_from": s["price"],
                    "duration_min": s["duration"],
                    "order": i,
                    "title": mk_title, "title_mk": mk_title, "title_en": en_title,
                    "short_desc": mk_short, "short_desc_mk": mk_short, "short_desc_en": en_short,
                    "full_desc": mk_full, "full_desc_mk": mk_full, "full_desc_en": en_full,
                    "what_included": mk_incl, "what_included_mk": mk_incl,
                    "what_included_en": en_incl,
                },
            )
        self.stdout.write(f"  {len(SERVICE_CATEGORIES)} categories, {len(SERVICES)} services")

    def _specialties(self):
        out = {}
        for slug, mk, en in SPECIALTIES:
            obj, _ = Specialty.objects.update_or_create(
                slug=slug,
                defaults={"name": mk, "name_mk": mk, "name_en": en},
            )
            out[slug] = obj
        self.stdout.write(f"  {len(SPECIALTIES)} specialties")
        return out

    def _trainers(self, specialties):
        out = {}
        for i, t in enumerate(TRAINERS):
            mk_role, mk_short, mk_bio, mk_cert = t["mk"]
            en_role, en_short, en_bio, en_cert = t["en"]
            member, _ = TeamMember.objects.update_or_create(
                slug=t["slug"],
                defaults={
                    "name": t["name"], "name_mk": t["name"], "name_en": t["name_en"],
                    "years_experience": t["years"],
                    "email": t["email"],
                    "order": i,
                    "is_active": True,
                    "role": mk_role, "role_mk": mk_role, "role_en": en_role,
                    "short_bio": mk_short, "short_bio_mk": mk_short, "short_bio_en": en_short,
                    "bio": mk_bio, "bio_mk": mk_bio, "bio_en": en_bio,
                    "certifications": mk_cert, "certifications_mk": mk_cert,
                    "certifications_en": en_cert,
                },
            )
            member.specialties.set([specialties[s] for s in t["specialties"]])
            out[t["slug"]] = member
        self.stdout.write(f"  {len(TRAINERS)} trainers")
        return out

    def _classes(self, trainers):
        sessions = 0
        for i, c in enumerate(CLASSES):
            mk_title, mk_short, mk_full, mk_ben = c["mk"]
            en_title, en_short, en_full, en_ben = c["en"]
            gym_class, _ = GymClass.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "trainer": trainers[c["trainer"]],
                    "intensity": c["intensity"],
                    "duration_min": c["duration"],
                    "capacity": c["capacity"],
                    "order": i,
                    "is_active": True,
                    "title": mk_title, "title_mk": mk_title, "title_en": en_title,
                    "short_desc": mk_short, "short_desc_mk": mk_short, "short_desc_en": en_short,
                    "full_desc": mk_full, "full_desc_mk": mk_full, "full_desc_en": en_full,
                    "benefits": mk_ben, "benefits_mk": mk_ben, "benefits_en": en_ben,
                },
            )
            for weekday, start, room in c["sessions"]:
                ClassSession.objects.update_or_create(
                    gym_class=gym_class,
                    weekday=weekday,
                    start_time=start,
                    defaults={
                        "room": room, "room_mk": room,
                        "room_en": ROOMS_EN[room],
                    },
                )
                sessions += 1
        self.stdout.write(f"  {len(CLASSES)} classes, {sessions} weekly sessions")

    def _plans(self):
        for i, p in enumerate(PLANS):
            mk_name, mk_tag, mk_period, mk_feat = p["mk"]
            en_name, en_tag, en_period, en_feat = p["en"]
            MembershipPlan.objects.update_or_create(
                slug=p["slug"],
                defaults={
                    "price": p["price"],
                    "is_featured": p["featured"],
                    "order": i,
                    "name": mk_name, "name_mk": mk_name, "name_en": en_name,
                    "tagline": mk_tag, "tagline_mk": mk_tag, "tagline_en": en_tag,
                    "period": mk_period, "period_mk": mk_period, "period_en": en_period,
                    "features": mk_feat, "features_mk": mk_feat, "features_en": en_feat,
                },
            )
        self.stdout.write(f"  {len(PLANS)} membership plans")

    def _blog(self, trainers):
        cats = {}
        for slug, mk, en, order in BLOG_CATEGORIES:
            cat, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": mk, "name_mk": mk, "name_en": en, "order": order},
            )
            cats[slug] = cat

        now = timezone.now()
        for p in POSTS:
            mk_title, mk_excerpt, mk_body = p["mk"]
            en_title, en_excerpt, en_body = p["en"]
            Post.objects.update_or_create(
                slug=p["slug"],
                defaults={
                    "category": cats[p["cat"]],
                    "author": trainers[p["author"]],
                    "published_at": now - timezone.timedelta(days=p["days_ago"]),
                    "is_published": True,
                    "title": mk_title, "title_mk": mk_title, "title_en": en_title,
                    "excerpt": mk_excerpt, "excerpt_mk": mk_excerpt, "excerpt_en": en_excerpt,
                    "body": mk_body, "body_mk": mk_body, "body_en": en_body,
                },
            )
        self.stdout.write(f"  {len(BLOG_CATEGORIES)} blog categories, {len(POSTS)} posts")

    def _testimonials(self):
        for t in TESTIMONIALS:
            mk_role, mk_text = t["mk"]
            en_role, en_text = t["en"]
            Testimonial.objects.update_or_create(
                author=t["author"],
                defaults={
                    "rating": t["rating"],
                    "is_featured": t["featured"],
                    "order": t["order"],
                    "author_mk": t["author"], "author_en": t["author_en"],
                    "role": mk_role, "role_mk": mk_role, "role_en": en_role,
                    "text": mk_text, "text_mk": mk_text, "text_en": en_text,
                },
            )
        self.stdout.write(f"  {len(TESTIMONIALS)} testimonials")

    def _faqs(self):
        for category, order, mk, en in FAQS:
            mk_q, mk_a = mk
            en_q, en_a = en
            FAQ.objects.update_or_create(
                question_mk=mk_q,
                defaults={
                    "category": category,
                    "order": order,
                    "question": mk_q, "question_en": en_q,
                    "answer": mk_a, "answer_mk": mk_a, "answer_en": en_a,
                },
            )
        self.stdout.write(f"  {len(FAQS)} FAQs")

    def _attach(self, obj, field, asset):
        src = SEED_ASSETS / f"{asset}.webp"
        if not src.exists():
            return False

        current = getattr(obj, field)
        filename = f"{asset}.webp"
        target = current.field.generate_filename(obj, filename)
        if current.name == target and current.storage.exists(target):
            return False

        if current.storage.exists(target):
            current.storage.delete(target)
        with src.open("rb") as fh:
            current.save(filename, File(fh), save=True)
        return True

    def _images(self):
        if not SEED_ASSETS.is_dir():
            self.stdout.write(self.style.WARNING("  seed_assets/ missing — skipping photos"))
            return

        written = 0
        written += self._attach(SiteSettings.load(), "hero_image", "hero")

        for service in Service.objects.all():
            written += self._attach(service, "image", f"service-{service.slug}")
            for n in (1, 2):
                if not (SEED_ASSETS / f"gallery-{service.slug}-{n}.webp").exists():
                    continue
                shot, _ = ServiceImage.objects.get_or_create(
                    service=service, order=n, defaults={"image": ""}
                )
                written += self._attach(shot, "image", f"gallery-{service.slug}-{n}")

        for gym_class in GymClass.objects.all():
            written += self._attach(gym_class, "image", f"class-{gym_class.slug}")

        for member in TeamMember.objects.all():
            written += self._attach(member, "photo", f"trainer-{member.slug}")

        for post in Post.objects.all():
            written += self._attach(post, "cover_image", f"post-{post.slug}")

        for n, testimonial in enumerate(Testimonial.objects.order_by("order", "pk"), start=1):
            written += self._attach(testimonial, "photo", f"testimonial-{n}")

        self.stdout.write(f"  {written} photos copied from seed_assets/")
