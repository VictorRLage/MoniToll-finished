package Dominio

data class Torre(var idTorre:Int, var SerialID:String, var SO:String, var Maquina:String,
                 var Processador:String, var Disco:String, var Ram:String, var fkEmpresa:Int) {
    constructor() : this(0,"", "","","","","",0)
}