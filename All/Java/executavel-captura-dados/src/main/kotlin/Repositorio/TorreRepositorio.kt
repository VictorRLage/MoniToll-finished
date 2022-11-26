package Repositorio

import Dominio.Torre
import Dominio.Usuario
import org.springframework.jdbc.core.BeanPropertyRowMapper
import org.springframework.jdbc.core.JdbcTemplate

class TorreRepositorio(val jdbcTemplate: JdbcTemplate) {
    fun ListarTorres(usuario:Usuario):List<Any>{
        val idTorres = jdbcTemplate.queryForList(
            "select idTorre from Torre where fkEmpresa = ?;",
            usuario.fkEmpresa,
        )
        return idTorres
    }
    fun VerificarSerialId(idTorre:Int):Torre{
        val erroTorre = Torre(0,"", "","","","","",0)
        val SerialId = jdbcTemplate.query(
            "select * from Torre where idTorre = ?;",
            BeanPropertyRowMapper(Torre::class.java),
            idTorre
        )

        if (SerialId.size == 0){
            println("ERRO TORRE")
            return erroTorre
        }else{
            return SerialId[0]
        }
    }

    fun UpdateTorre(torre:Torre){
        jdbcTemplate.update("UPDATE Torre SET SerialID = ?,  SO = ?, Maquina = ?, Processador = ?, Disco = ?, RAM = ?,  fkEmpresa = ? WHERE idTorre = ?;",
            torre.SerialID, torre.SO, torre.Maquina, torre.Processador, torre.Disco, torre.Ram, torre.fkEmpresa, torre.idTorre
        )
    }
}