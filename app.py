from flask import Flask, render_template, request, url_for, redirect, session
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine
from models import Book, User

app = Flask(__name__)
app.secret_key = "inominavel"
Base.metadata.create_all(engine)


@app.route('/')
def index():
    with Session(bind=engine) as session:
        usuarios = session.scalars(select(User)).all()
        livros = session.scalars(select(Book)).all()
    return render_template('index.html', usuarios=usuarios, livros=livros)


@app.route('/usuario/novo', methods=['POST', 'GET'])
def form_usuario():
    if request.method == 'POST':
        usuario = User(
            nome=request.form.get('nome'),
            email=request.form.get('email')
        )
        with Session(bind=engine) as session:
            session.add(usuario)
            session.commit()
        
        return redirect(url_for('index'))
    return render_template('form_usuario.html')


@app.route('/livros/novo', methods=['GET', 'POST'])
def form_livro():
    if request.method == 'POST':
        with Session() as session:
            usuario_id = session.scalar(select(User.id).where(User.nome == request.form['usuario']))
            livro = Book(
                titulo=request.form.get('titulo'),
                usuario_id=usuario_id,
            )
            session.add(livro)
            session.commit()
            return redirect(url_for('index'))
    return render_template('form_livro.html')

@app.route('/livros/listar', methods=['GET'])
def listar_livros():
    with Session(bind=engine) as session:
        statement = select(Book).order_by(Book.titulo)
        livros = session.scalars(statement).all()

        return render_template('index.html', livros=livros)

@app.route('/usuarios/listar', methods=['GET'])
def listar_usuarios():
    with Session(bind=engine) as session:
        statement = select(User).order_by(User.nome)
        usuarios = session.scalars(statement).all()

        return render_template('index.html', usuarios=usuarios)
        
if __name__ == "__main__":
    app.run(debug=True)