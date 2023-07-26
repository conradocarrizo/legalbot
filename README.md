LEGALBOT
======

Desafio Backend


### Endpoint Requeridos ###

* Crear una sociedad: Un endpoint que permita crear una nueva sociedad. Una sociedad tiene al menos un nombre y un RUT.

Endpoint POST api/societies/

   body de ejemplo
   ```
    {
        "rut": {
            "code": "12345628-k",
            "name": "Empresa Name" 
        },
        "actions": 100
    }
   ```
   response de ejemplo 201
   ```
   {
        "id": 3,
        "rut": {
            "id": 31,
            "created_at": "2023-07-26T06:00:34.585075Z",
            "updated_at": "2023-07-26T06:00:34.585102Z",
            "code": "12345628-k",
            "name": "Empresa Name"
        },
        "created_at": "2023-07-26T06:00:34.588512Z",
        "updated_at": "2023-07-26T06:00:34.588530Z",
        "actions": 100,
        "members": [],
        "admins": []
    }
   ```


* Crear un socio: Un endpoint que permita crear un nuevo socio dentro de una sociedad. Un socio tiene al menos un nombre, RUT, dirección y participación

Endpoint POST api/societies/{society_pk}/create_member/

   body de ejemplo
   ```
    {
        "rut": {
            "code": "12212018-c",
            "name": "Persona Name"
        },
        "address": "Avenida Siempre Viva 2132",
        "actions": 1200
    }
   ```
   response de ejemplo 201
   ```
    {
        "message": "Miembro agregado exitosamente",
        "member_id": 26
    }
   ```

* Crear un administrador: Un endpoint que permita crear un administrador dentro de una sociedad. Un administrador tiene al menos un nombre, RUT y una lista de facultades como "Abrir una cuenta corriente", "Firmar cheques" o "Firmar contratos".

Endpoint POST api/societies/{society_pk}/create_admin/

   body de ejemplo
   ```
    {
        "rut": {
            "code": "12345678-9",
            "name": "Persona 20"
        },
        "address": "Avenida Siempre Viva 2132",
        "faculties": ["firmar checkes", "administrar"]
    }
   ```
   response de ejemplo 201
   ```
    {
        "message": "Admin agregado exitosamente",
        "admin_id": 27
    }
   ```

* Eliminar una sociedad: Un endpoint que permita eliminar una sociedad existente.
    Endpoint DELETE api/societies/{society_pk}/

* Obtener sociedades que contengan al socio o al administrador con el RUT indicado: Un endpoint que devuelva todas las sociedades en las que está asociado un socio o administrador específico. El RUT del socio o administrador se pasará como parámetro en la URL.

    Endpoint GET api/societies/list_by_person_rut/?rut={rut_socio_admin}

   response de ejemplo 200
   ```
    {
        "rut": {
            "id": 26,
            "created_at": "2023-07-25T20:40:20.654527Z",
            "updated_at": "2023-07-25T20:40:20.654543Z",
            "code": "12212118-a",
            "name": "Persona 1"
        },
        "admin_societies": [
            {
                "name": "Admin Name",
                "rut": "12345678-9",
                "faculties": [
                    "firmar checkes",
                    "administrar"
                ]
            }
        ],
        "member_societies": [
            {
                "name": "Miembro Name",
                "rut": "12345678-9",
                "porcentage": "10%"
            }
        ]
    }
   ```

* Obtener socios y administradores que están en la sociedad con el RUT indicado: Un endpoint que devuelva todos los socios y administradores que están asociados a una sociedad específica.

   Endpoint GET api/societies/?rut={society_rut}

   response de ejemplo 200
   ```
    [
        {
            "id": 1,
            "rut": {
                "id": 1,
                "created_at": "2023-07-25T09:35:23.484117Z",
                "updated_at": "2023-07-25T09:35:23.484135Z",
                "code": "12345678-9",
                "name": "Empresa 1"
            },
            "admins": [
                {
                    "id": 1,
                    "admin": {
                        "id": 24,
                        "rut": {
                            "id": 28,
                            "created_at": "2023-07-25T20:54:42.441055Z",
                            "updated_at": "2023-07-25T20:54:42.441076Z",
                            "code": "12212118-c",
                            "name": "Persona 2"
                        },
                        "created_at": "2023-07-25T20:54:42.442095Z",
                        "updated_at": "2023-07-25T20:54:42.442112Z",
                        "address": "Avenida Siempre Viva 2132"
                    },
                    "created_at": "2023-07-25T20:54:42.443703Z",
                    "updated_at": "2023-07-25T20:54:42.443729Z",
                    "faculties": [
                        "firmar checkes",
                        "administrar"
                    ],
                    "society": 1
                },
                {
                    "id": 2,
                    "admin": {
                        "id": 25,
                        "rut": {
                            "id": 30,
                            "created_at": "2023-07-26T03:59:24.809626Z",
                            "updated_at": "2023-07-26T03:59:24.809656Z",
                            "code": "12342678-9",
                            "name": "Persona 20"
                        },
                        "created_at": "2023-07-26T03:59:24.814327Z",
                        "updated_at": "2023-07-26T03:59:24.814355Z",
                        "address": "Avenida Siempre Viva 2132"
                    },
                    "created_at": "2023-07-26T03:59:24.816383Z",
                    "updated_at": "2023-07-26T03:59:24.816402Z",
                    "faculties": [
                        "firmar checkes",
                        "administrar"
                    ],
                    "society": 1
                }
            ],
            "members": [
                {
                    "id": 1,
                    "member": {
                        "id": 22,
                        "rut": {
                            "id": 26,
                            "created_at": "2023-07-25T20:40:20.654527Z",
                            "updated_at": "2023-07-25T20:40:20.654543Z",
                            "code": "12212118-a",
                            "name": "Persona 1"
                        },
                        "created_at": "2023-07-25T20:40:20.655473Z",
                        "updated_at": "2023-07-25T20:40:20.655482Z",
                        "address": "Avenida Siempre Viva 2132"
                    },
                    "participation": "1200.0%",
                    "created_at": "2023-07-25T20:40:20.656347Z",
                    "updated_at": "2023-07-25T20:40:20.656356Z",
                    "actions": 1200,
                    "society": 1
                },
                {
                    "id": 2,
                    "member": {
                        "id": 23,
                        "rut": {
                            "id": 27,
                            "created_at": "2023-07-25T20:45:49.475822Z",
                            "updated_at": "2023-07-25T20:45:49.475844Z",
                            "code": "12212118-b",
                            "name": "Persona 2"
                        },
                        "created_at": "2023-07-25T20:45:49.476940Z",
                        "updated_at": "2023-07-25T20:45:49.476949Z",
                        "address": "Avenida Siempre Viva 2132"
                    },
                    "participation": "1200.0%",
                    "created_at": "2023-07-25T20:45:49.477926Z",
                    "updated_at": "2023-07-25T20:45:49.477935Z",
                    "actions": 1200,
                    "society": 1
                }
            ],
            "created_at": "2023-07-25T09:35:23.486845Z",
            "updated_at": "2023-07-25T09:35:23.486855Z",
            "actions": 100
        }
    ]
   ```

