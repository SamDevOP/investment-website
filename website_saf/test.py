from passlib.hash import pbkdf2_sha256


s=pbkdf2_sha256("password")

pbkdf2_sha256.verify("password",s)

