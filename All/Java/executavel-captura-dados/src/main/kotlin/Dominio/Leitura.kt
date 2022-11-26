package Dominio

data class Leitura(var id:Int, var Leitura:Double, var DataHora:String, var fkTorre:Int, var fkComponentes:Int) {
    constructor() : this(0,0.0, "", 0, 0)
}