<?php

function rot13($string)
{
    $rot13 = str_rot13($string);
    return $rot13;
}
$flag = getenv("FLAG1");
$db = [];
$db['admin'] =  [
    "geslo" => "ZeloDolgoInVarnoGeslo3",
    "posta" => [
        [
            "from" => "programer",
            "subject" => "Pozdrav",
            "message" => "Zdravo, v redu sem."
        ],
        [
            "from" => "programer",
            "subject" => "Potrdilo",
            "message" => "Delo je v redu."
        ],
        [
            "from" => "višji admin",
            "subject" => "Zastava",
            "message" => ("IKT Zastava\n<span>$flag</span>\nje na mestu.")
        ]
    ]
];

$db["programer"] = [
    "geslo" => "JoskoJarc",
    "posta" => [
        [
            "from" => "Tadej",
            "subject" => "Pozdrav",
            "message" => "Zdravo, kako si?"
        ],
        [
            "from" => "Jernej",
            "subject" => "Cezar",
            "message" => "Zadnjič sem bral en res dober članek od cezarja! Veš da je že on poznal kriptografijo?"
        ],
        [
            "from" => "Jernej",
            "subject" => "Dostop",
            "message" => "Šef me je prosil, če ti pošljem dostop do portala. Poslal sem ti kar njegovo admin geslo, ampak sem ga zakriptiral, kot sva se zmenila, da ga ne morejo dobiti hekerji:\n\n<span><b>" . rot13($db["admin"]["geslo"])
                . "</b></span>"
        ],
        [
            "from" => "Martin",
            "subject" => "Napaka!",
            "message" => "Zadnjič me je zmotil tvoj program, prosim popravi ga!"
        ],
        [
            "from" => "žena",
            "subject" => "Ločitev",
            "message" => "Jaz bom vzela otroke, ti pa lahko obdržiš televizijo."
        ]
    ]
];
