{
    "length": {
        "type": "int",
        "default": 20,
        "required": true,
        "comment": "Password Length"
    },
    "letters": {
        "type": "str",
        "default": "printable",
        "required": true,
        "comment": "Type of characters to use in password values",
        "values": [ "printable", "ascii_letters", "digits" ]
    }
}