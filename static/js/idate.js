$("#btnModal").on("click",function(){
    $("#modal-date").modal();
})

$('.jd-date').datepicker({
    format: "dd/mm/yyyy",
    languaje: "es",    
    startDate: "-200y",
    endDate: "+0d",
    orientation: "auto",
    autoclose: true
});