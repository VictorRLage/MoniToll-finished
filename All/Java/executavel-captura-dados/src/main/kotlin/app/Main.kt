package app

import Config.Conexao
import Dominio.Leitura
import Dominio.Torre
import Dominio.TorreComponente
import Dominio.Usuario
import Repositorio.LeituraRepositorio
import Repositorio.TorreComponenteRepositorio
import Repositorio.TorreRepositorio
import Repositorio.UsuarioRepositorio
import com.github.britooo.looca.api.core.Looca
import java.io.BufferedReader
import java.io.InputStreamReader
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.*
import javax.swing.JOptionPane
import javax.swing.JOptionPane.*

open class Main {
    companion object {
        @JvmStatic fun main(args: Array<String>) {

            // Configurar repositorios
            val jdbcTemplate = Conexao().getJdbcTemplate()
            val usuarioRepositorio = UsuarioRepositorio(jdbcTemplate)
            val torreRepositorio = TorreRepositorio(jdbcTemplate)
            val torreComponenteRepositorio = TorreComponenteRepositorio(jdbcTemplate)
            val leituraRepositorio = LeituraRepositorio(jdbcTemplate)

            //Configurar looca
            val looca = Looca()
            val sistema = looca.sistema
            val processador = looca.processador
            val grupoDiscos = looca.grupoDeDiscos
            val discos = grupoDiscos.discos
            val memoria = looca.memoria

            // deseja fazer login?
            val fazerLogin = showConfirmDialog(
                null, """Bem vindo ao Green Light
        |Deseja fazer Login?
    """.trimMargin()
            )
            if (fazerLogin != 0){
                System.exit(0)
            }
            // vericação login e pegar fkEmpresa
            val email = showInputDialog(null, "Qual o seu e-mail").toString()
            val senha = showInputDialog(null, "Qual a senha?").toString()

            val Usuario = usuarioRepositorio.Logar(email, senha)
            if (Usuario.fkEmpresa == 0){
                showMessageDialog(
                    null, """Erro ao efetuar login
            |Por favor tente novamente
        """.trimMargin()
                )
                System.exit(0)
            }
            val novoUsuario = Usuario(email,senha,Usuario.fkEmpresa)

            println("fkEmpresa: " + novoUsuario.fkEmpresa)

            // pegar torres dessa empresa
            val idTorres = torreRepositorio.ListarTorres(novoUsuario)
            var consulta = "\n"

            println("Torres: "+idTorres)

            idTorres.forEach {
                val id = it.toString()
                val idReplace = id.replace("{idTorre=","")
                val idReplaceAfter = idReplace.replace("}","")
                consulta += "id: ${idReplaceAfter}"
                consulta += "\r\n"
            }




            // escolher a torre
            val idTorre = showInputDialog(null, "Qual é essa torre?" + consulta).toInt()






            var contador = 0
            fun InserirLeitura() {
                println("Agora sao ${LocalDateTime.now()}")
                Timer().schedule(object : TimerTask() {
                    override fun run() {



                        val torre = torreRepositorio.VerificarSerialId(idTorre)
                        if (torre.idTorre == 0){
                            showMessageDialog(
                                null, """Erro ao selecionar torre
                        |Por favor digite um id valido
                        """.trimMargin()
                            )
                            System.exit(0)
                        }
                        // torre não possui dados
                        if (torre.SerialID == ""){
                            println("Torre não possui dados")
                            showMessageDialog(
                                null, """Os dados dessa torre ainda não foram cadastrados
                        |Vamos cadastrar!
                        """.trimMargin()
                            )

                            // Pegando serial id
                            val serialIdCmd = ProcessBuilder(
                                "cmd.exe", "/c", "cd \"C:\\Users\" && wmic bios get serialnumber"
                            )
                            serialIdCmd.redirectErrorStream(true)
                            val serialIdCmd_start = serialIdCmd.start()
                            val serialIdCmd_stream = BufferedReader(InputStreamReader(serialIdCmd_start.inputStream))
                            val serialIdCmd_line = serialIdCmd_stream.readLines()
                            val serialId = serialIdCmd_line[2]
                            println("SerialId: "+serialId)

                            // Pegando sistema operacional
                            val so = sistema.sistemaOperacional
                            println("SO: "+so)

                            // Pegando modelo maquina
                            val maquinaCmd = ProcessBuilder(
                                "cmd.exe", "/c", "cd \"C:\\Users\" && wmic computersystem get model"
                            )
                            maquinaCmd.redirectErrorStream(true)
                            val maquinaCmd_start = maquinaCmd.start()
                            val maquinaCmd_stream = BufferedReader(InputStreamReader(maquinaCmd_start.inputStream))
                            val maquinaCmd_line = maquinaCmd_stream.readLines()
                            val maquina = maquinaCmd_line[2]
                            println("Maquina: "+maquina)

                            // Pegando processador
                            val processador = processador.nome
                            println("Processador: "+processador)

                            // Pegando processador
                            val discoStr = (discos[0].modelo).toString()
                            val disco = discoStr.replace("(Unidades de disco padrão)","")
                            println("Disco: "+disco)

                            // Pegando ram
                            val ramCmd = ProcessBuilder(
                                "cmd.exe", "/c", "cd \"C:\\Users\" &&wmic memorychip get devicelocator"
                            )
                            ramCmd.redirectErrorStream(true)
                            val ramCmd_start = ramCmd.start()
                            val ramCmd_stream = BufferedReader(InputStreamReader(ramCmd_start.inputStream))
                            val ramCmd_line = ramCmd_stream.readLines()
                            val ram = ramCmd_line[2]
                            println("RAM: "+ram)

                            val novoTorre = Torre(idTorre, serialId, so, maquina, processador,disco, ram, novoUsuario.fkEmpresa)
                            torreRepositorio.UpdateTorre(novoTorre)
                        }else{
                            // ja esta cadastrada vamos inserir dados
                            val inserir = showConfirmDialog(
                                null, """Os dados dessa torre já estão cadastrados!
                            |Deseja capturar e inserir a leitura?
                            """.trimMargin()
                            )
                            if (inserir != 0){
                                System.exit(0)
                            }

                            //Pegar lista de componentes
                            val nonoTorreComponente = TorreComponente(idTorre,0)
                            val fkComponentes = torreComponenteRepositorio.ListarComponentes(nonoTorreComponente)


                            fkComponentes.forEach {
                                val fkComponenteStr = it.toString()
                                val ifkComponenteReplace = fkComponenteStr.replace("{fkComponente=","")
                                val fkComponenteReplaceAfter = ifkComponenteReplace.replace("}","")
                                val fkComponente = fkComponenteReplaceAfter.toInt()

                                var leitura = 0.0
                                if(fkComponente == 1){
                                    leitura = (processador.numeroCpusLogicas).toDouble()
                                }else if(fkComponente == 2){
                                    leitura = (processador.uso)
                                }else if(fkComponente == 3){
                                    leitura = memoria.total.toDouble()/1024/1024/1024
                                }else if(fkComponente == 4){
                                    leitura = memoria.emUso.toDouble()/1024/1024/1024
                                }else if(fkComponente == 5){
                                    leitura = ((memoria.emUso.toDouble()/1024/1024/1024)*100)/(memoria.total.toDouble()/1024/1024/1024)
                                }else if(fkComponente == 6){
                                    leitura = discos[0].tamanho.toDouble()/1024/1024/1024
                                }
                                println("Leitura: "+leitura)
                                val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
                                val dataHora = (LocalDateTime.now().format(formatter)).toString()
                                val novaLeitura = Leitura(0,leitura,dataHora, idTorre, fkComponente)
                                leituraRepositorio.insertLeitura(novaLeitura)
                            }

                        }
                        InserirLeitura()
                    }
                }, 10000)
            }
            InserirLeitura()

        }
    }
}