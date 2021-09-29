$(document).ready(function(){
    if ($("#pedigree_select").val() == "new_pedigree") {
        $("#pedigree_input").show();
    } else {
        $("#pedigree_input").hide();
    }
    
    $("#pedigree_select").change(function() {
        if ($("#pedigree_select").val() == "new_pedigree") {
            $("#pedigree_input").show();
        } else {
            $("#pedigree_input").hide();
        }
    });
});

$(document).ready(function(){
    if ($("#experiment_select").val() == "new_experiment") {
        $("#experiment_input").show();
    } else {
        $("#experiment_input").hide();
    }
    
    $("#experiment_select").change(function() {
        if ($("#experiment_select").val() == "new_experiment") {
            $("#experiment_input").show();
        } else {
            $("#experiment_input").hide();
        }
    });
});

$(document).ready(function(){
    if ($("#status_select").val() == "new_status") {
        $("#status_input").show();
    } else {
        $("#status_input").hide();
    }
    
    $("#status_select").change(function() {
        if ($("#status_select").val() == "new_status") {
            $("#status_input").show();
        } else {
            $("#status_input").hide();
        }
    });
});