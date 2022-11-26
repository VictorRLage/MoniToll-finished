package Repositorio

import Dominio.TorreComponente
import Dominio.Usuario
import org.springframework.jdbc.core.JdbcTemplate

class TorreComponenteRepositorio(val jdbcTemplate: JdbcTemplate) {
    fun ListarComponentes(torreComponente: TorreComponente):List<Any>{
        val idTorres = jdbcTemplate.queryForList(
            "select fkComponente from Torre_Componente where fkTorre = ?;",
            torreComponente.fkTorre,
        )
        return idTorres
    }
}