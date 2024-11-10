@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:UserBase,roles: list[int]):
    try:
            """
            this funtion receives the  request sent from  register users form and will saved on databes,use the tables users,roles, roles_users  , it  function should validate if user exist,if user email exits and rol_id exits,so return errors
            """        
            create_user_model =Users(
                  name = create_user_request.name,
                  username=create_user_request.username,
                  email = create_user_request.email,
                  hashed_password = bcrypt_context.hash(create_user_request.password),
                  
            )
            #save users
            db.add(create_user_model)
            db.commit()

            if create_user_model.id is not None: #e
                print(create_user_model.id)
                for rol_id in roles:
                    # save the users whit the id_rol
                    role_usuario = UserRoles(usuario_id=create_user_model.id, rol_id=rol_id)
                    db.add(role_usuario)
           
                db.commit()
                return {"data": "success" ,"status_code":200,"details": "Registro aplicado con exito"}
            else:
                return {"data": "error" ,"status_code":401,"details": "Error al intentar aplicar registo"}
               # db.add(role_usuario)

            #db.add(create_user_model)
            #db.add(create_user_model)
            
            #db.commit()
    except Exception as e:
        print(f"Error al crear el usuario: {str(e)}")
        
        raise ValueError("Error al crear el usuario. Por favor, verifica los datos.")
    
