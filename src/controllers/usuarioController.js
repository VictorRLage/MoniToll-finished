var usuarioModel = require("../models/usuarioModel");

var sessoes = [];

function testar(req, res) {
    console.log("ENTRAMOS NA usuarioController");
    res.json("ESTAMOS FUNCIONANDO!");
}

function listar(req, res) {
    usuarioModel.listar()
        .then(function (resultado) {
            if (resultado.length > 0) {
                res.status(200).json(resultado);
            } else {
                res.status(204).send("Nenhum resultado encontrado!")
            }
        }).catch(
            function (erro) {
                console.log(erro);
                console.log("Houve um erro ao realizar a consulta! Erro: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
            );
}
        
function entrar(req, res) {
            var email = req.body.emailServer;
            var senha = req.body.senhaServer;
            
            if(email == undefined) {
                res.status(400).send("Seu email está undefined!");
            } else if (senha == undefined) {
                res.status(400).send("Sua senha está indefinida!");
            } else {
                
        usuarioModel.entrar(email, senha)
            .then(
                function (resultado) {
                    console.log(`\nResultados encontrados: ${resultado.length}`);
                    console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

                    if (resultado.length == 1) {
                        console.log(resultado);
                        res.json(resultado[0]);
                    } else if (resultado.length == 0) {
                        res.status(403).send("Email e/ou senha inválido(s)");
                    } else {
                        res.status(403).send("Mais de um usuário com o mesmo login e senha!");
                    }
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log("\nHouve um erro ao realizar o login! Erro: ", erro.sqlMessage);
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }

}
function verificarPlano(req, res) {
    var fkEmpresa = req.body.fkEmpresaServer;
    
    if(fkEmpresa == undefined) {
        res.status(400).send("Seu email está undefined!");
    }else {
        
usuarioModel.verificarPlano(fkEmpresa)
    .then(
        function (resultado) {
            console.log(`\nResultados encontrados: ${resultado.length}`);
            console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

            if (resultado.length != 0) {
                console.log(resultado);
                res.json(resultado[0]);
            } else if (resultado.length == 0) {
                res.status(403).send("Não tem plano/empresa");
            }
        }
    ).catch(
        function (erro) {
            console.log(erro);
            console.log("\nHouve um erro ao verificar plano! Erro: ", erro.sqlMessage);
            res.status(500).json(erro.sqlMessage);
        }
    );
}
}

function cadastrar(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var nome = req.body.nomeServer;
    var cpf = req.body.cpfServer;
    var email = req.body.emailServer;
    var senha = req.body.senhaServer;
    var perfil = req.body.fkPerfilServer;

    // Faça as validações dos valores
    if (nome == undefined) {
        res.status(400).send("Seu nome está undefined!");
    } else if (cpf == undefined) {
        res.status(400).send("Seu cpf está undefined!");
    } else if (email == undefined) {
        res.status(400).send("Sua email está undefined!");
    } else if (senha == undefined) {
        res.status(400).send("Seu senha está undefined!");
    } else if (perfil == undefined) {
        res.status(400).send("Seu perfil está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.cadastrar(nome, cpf, email, senha, perfil)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function CadastrarUsuario(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var nome = req.body.nomeServer;
    var email = req.body.emailServer;
    var senha = req.body.senhaServer;
    var fkPerfil = req.body.fkPerfilServer;
    var fkEmpresa = req.body.fkEmpresaServer;

    // Faça as validações dos valores
    if (nome == undefined) {
        res.status(400).send("Seu nome está undefined!");
    } else if (email == undefined) {
        res.status(400).send("Sua email está undefined!");
    } else if (senha == undefined) {
        res.status(400).send("Seu senha está undefined!");
    } else if (fkPerfil == undefined) {
        res.status(400).send("Seu fkPerfil está undefined!");
    } else if (fkEmpresa == undefined) {
        res.status(400).send("Seu fkEmpresa está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.CadastrarUsuario(nome, email, senha, fkPerfil, fkEmpresa)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function CadastrarTorre(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var fkEmpresa = req.body.fkEmpresaServer;
    var loc = req.body.locServer;

    // Faça as validações dos valores
    if (fkEmpresa == undefined) {
        res.status(400).send("Seu fkEmpresa está undefined!");
    } else if (loc == undefined) {
        res.status(400).send("Seu loc está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.CadastrarTorre(loc,fkEmpresa)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro da torre! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}


function CadastrarComponente(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var fkTorre = req.body.fkTorreServer;
    var fkComponente = req.body.fkComponenteServer;

    // Faça as validações dos valores
    if (fkTorre == undefined) {
        res.status(400).send("Seu fkTorre está undefined!");
    } else if (fkComponente == undefined) {
        res.status(400).send("Seu fkComponente está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.CadastrarComponente(fkTorre,fkComponente)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro da torre! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function cadastrarEmp(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var idEmp = req.body.idEmpServer;
    var nomeEmp = req.body.nomeEmpServer;
    var plano = req.body.planoServer;
    var cnpjEmp = req.body.cnpjEmpServer;
    var emailEmp = req.body.emailEmpServer;

    // Faça as validações dos valores
    if (idEmp == undefined) {
        res.status(400).send("Seu idEmp está undefined!");
    } else if (nomeEmp == undefined) {
        res.status(400).send("Seu nomeEmp está undefined!");
    }else if (plano == undefined) {
        res.status(400).send("Seu plano está undefined!");
    }else if (cnpjEmp == undefined) {
        res.status(400).send("Seu cnpjEmp está undefined!");
    }else if (emailEmp == undefined) {
        res.status(400).send("Seu emailEmp está undefined!");
    }else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.cadastrarEmp(idEmp, nomeEmp, plano, cnpjEmp, emailEmp)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function atualizarAdm(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var idEmp = req.body.idEmpServer;
    var EmailAdm = req.body.EmailAdmServer;

    // Faça as validações dos valores
    if (idEmp == undefined) {
        res.status(400).send("Seu idEmp está undefined!");
    } else if (EmailAdm == undefined) {
        res.status(400).send("Seu EmailAdm está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.atualizarAdm(idEmp, EmailAdm)
            .then(
                function (resultado) {
                        res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }}
function verificarTorres(req, res) {
    var fkEmpresa = req.body.fkEmpresaServer;
    
    if(fkEmpresa == undefined) {
        res.status(400).send("Seu email está undefined!");
    }else {
        
usuarioModel.verificarTorres(fkEmpresa)
    .then(
        function (resultado) {
            console.log(`\nResultados encontrados: ${resultado.length}`);
            console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

            if (resultado.length != 0) {
                console.log(resultado);
                res.json(resultado);
            } else if (resultado.length == 0) {
                res.status(403).send("Não tem torre");
            }
        }
    ).catch(
        function (erro) {
            console.log(erro);
            console.log("\nHouve um erro ao realizar o login! Erro: ", erro.sqlMessage);
            res.status(500).json(erro.sqlMessage);
        }
    );
}}

function ObterDadosTorre(req, res) {
    var idTorre = req.body.idTorreServer;
    
    if(idTorre == undefined) {
        res.status(400).send("Seu idTorre está undefined!");
    }else {
        
usuarioModel.ObterDadosTorre(idTorre)
    .then(
        function (resultado) {
            console.log(`\nResultados encontrados: ${resultado.length}`);
            console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

            if (resultado.length != 0) {
                console.log(resultado);
                res.json(resultado);
            } else if (resultado.length == 0) {
                res.status(403).send("Não tem torre");
            }
        }
    ).catch(
        function (erro) {
            console.log(erro);
            console.log("\nHouve um erro ao realizar o encontrar torres! Erro: ", erro.sqlMessage);
            res.status(500).json(erro.sqlMessage);
        }
    );
}}

function UltimaTorre(req, res) {
    var fkEmpresa = req.body.fkEmpresaServer;
    
    if(fkEmpresa == undefined) {
        res.status(400).send("Seu fkEmpresa está undefined!");
    }else {
        
usuarioModel.UltimaTorre(fkEmpresa)
    .then(
        function (resultado) {
            console.log(`\nResultados encontrados: ${resultado.length}`);
            console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

            if (resultado.length != 0) {
                console.log(resultado);
                res.json(resultado[resultado.length - 1]);
            } else if (resultado.length == 0) {
                res.status(403).send("Não tem torre");
            }
        }
    ).catch(
        function (erro) {
            console.log(erro);
            console.log("\nHouve um erro ao realizar o login! Erro: ", erro.sqlMessage);
            res.status(500).json(erro.sqlMessage);
        }
    );
}}





function ObterComponentes(req, res) {
    var fkTorre = req.body.fkTorreServer;
    
    if(fkTorre == undefined) {
        res.status(400).send("Seu fkTorre está undefined!");
    }else {
        
usuarioModel.ObterComponentes(fkTorre)
    .then(
        function (resultado) {
            console.log(`\nResultados encontrados: ${resultado.length}`);
            console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

            if (resultado.length != 0) {
                console.log(resultado);
                res.json(resultado);
            } else if (resultado.length == 0) {
                res.status(403).send("Não tem componentes");
            }
        }
    ).catch(
        function (erro) {
            console.log(erro);
            console.log("\nHouve um erro ao verificar plano! Erro: ", erro.sqlMessage);
            res.status(500).json(erro.sqlMessage);
        }
    );
}
}



module.exports = {
    entrar,
    cadastrar,
    listar,
    testar,
    cadastrarEmp,
    atualizarAdm,
    verificarTorres,
    verificarPlano,
    CadastrarTorre,
    UltimaTorre,
    CadastrarComponente,
    ObterComponentes,
    CadastrarUsuario,
    ObterDadosTorre
}