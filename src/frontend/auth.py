def autenticar(usuario, senha):
    if usuario == "aluno" and senha == "123":
        return "aluno"
    elif usuario == "professor" and senha == "123":
        return "professor"
    else:
        return None