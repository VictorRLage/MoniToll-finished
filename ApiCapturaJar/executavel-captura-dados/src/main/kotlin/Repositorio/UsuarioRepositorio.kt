package Repositorio

import Dominio.Torre
import Dominio.Usuario
import org.springframework.jdbc.core.BeanPropertyRowMapper
import org.springframework.jdbc.core.JdbcTemplate

class UsuarioRepositorio(val jdbcTemplate: JdbcTemplate) {

    fun Logar(email:String, senha:String):Usuario{

        val erroUsuario = Usuario("","",0)
        val Usuario = jdbcTemplate.query(
            "select * from Usuario where Email = ? and Senha = ?;",
            BeanPropertyRowMapper(Usuario::class.java),
            email, senha
        )
        if (Usuario.size == 0){
            println("ERRO USUARIO")
            return erroUsuario
        }else{
            return Usuario[0]
        }
    }


}