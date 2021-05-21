$(document).ready(function () {
    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }
    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    });
    $.fn.pressEnter = function(fn) {  
      return this.each(function() {  
          $(this).bind('enterPress', fn);
          $(this).keyup(function(e){
              if(e.keyCode == 13)
              {
                $(this).trigger("enterPress");
              }
          })
      });  
    }; 
    function fileClicked(){
        var previousFile = $(".selected_button_file_tree");
        if (previousFile.length){
            previousFile.removeClass("selected_button_file_tree");
            previousFile.addClass("not_selected_button_file_tree");
        }
        var previousDictionary = $(".selected_button_directory");
        previousDictionary.removeClass("selected_button_directory");
        previousDictionary.addClass("not_selected_button_directory");
    
        $(this).addClass("selected_button_file_tree");
        $(this).removeClass("not_selected_button_file_tree");
        id = $(this).attr("id");
        var newDictionary = $("#" + id.substring(0, id.search("_")));
        newDictionary.removeClass("not_selected_button_directory");
        newDictionary.addClass("selected_button_directory");
    
        $.post("/select", { "selected": $(this).attr('id') }, function (data) {
            $("#code").val(data["code"]);
        });
    }

    function directoryClicked(){
        var previousFile = $(".selected_button_file_tree");
        if (previousFile.length){
            previousFile.removeClass("selected_button_file_tree");
            previousFile.addClass("not_selected_button_file_tree");
        }
        var previousDictionary = $(".selected_button_directory");
        previousDictionary.removeClass("selected_button_directory");
        previousDictionary.addClass("not_selected_button_directory");

        $(this).removeClass("not_selected_button_directory");
        $(this).addClass("selected_button_directory");

        $.post("/select", { "selected": $(this).attr('id') }, function (data) {
            $("#code").val(data["code"]);
            $(data['id']).addClass("selected_button_file_tree");
            $(data['id']).removeClass("not_selected_button_file_tree");
        });
    }
    function newFileFormPressedEnter(){
        var that = this;
        var name = $(this).val();
        var selectedDirectory = $(".selected_button_directory").attr("id");
        $.post("/newFile", { name: name, selectedDirectory:  selectedDirectory}, function (data) {
            var $newFile = $("<button>", {id: data["id"], "class": "not_selected_button_file_tree"});
            $newFile.text(name +".c")
            $newFile.click(function () {
                fileClicked();
            });

            $("#dir" + selectedDirectory).append($newFile);
            $(that).hide();
        });
    }

    $(".selected_button_new_file").hide();
    $("#newFileDiv").hide();
    $("#nameOfNewDirectory").hide();
    $("#proversDiv").hide();
    $("#vcsDiv").hide();
    $("#resultButtonNotSelected").hide();
    $("#vcsButtonSelected").hide();
    $("#proversButtonSelected").hide();
    $("#Z3ButtonSelected").hide();
    $("#CVC4ButtonSelected").hide();
    $("#Alt-ErgoButtonSelected").hide();
    $(".selected_button_new_file").pressEnter(function () {
        newFileFormPressedEnter();
    });
    $("#newFileButton").click(function () { 
        var selectedDirectory = $(".selected_button_directory").attr("id");
        $("#newFile" + selectedDirectory).show();
    });
    $("#newDirectoryButton").click(function () { $("#nameOfNewDirectory").show(); });
    $("#proversButtonNotSelected").click(function () {
        $("#proversDiv").show();
        $("#resultDiv").hide();
        $("#vcsDiv").hide();

        $("#proversButtonSelected").show();
        $("#vcsButtonSelected").hide();
        $("#resultButtonSelected").hide();

        $("#proversButtonNotSelected").hide();
        $("#vcsButtonNotSelected").show();
        $("#resultButtonNotSelected").show();
    });
    $("#resultButtonNotSelected").click(function () {
        $("#proversDiv").hide();
        $("#vcsDiv").hide();
        $("#resultDiv").show();

        $("#proversButtonSelected").hide();
        $("#vcsButtonSelected").hide();
        $("#resultButtonSelected").show();

        $("#proversButtonNotSelected").show();
        $("#vcsButtonNotSelected").show();
        $("#resultButtonNotSelected").hide()();
    });
    $("#vcsButtonNotSelected").click(function () {
        $("#proversDiv").hide();
        $("#vcsDiv").show();
        $("#resultDiv").hide();

        $("#proversButtonSelected").hide();
        $("#vcsButtonSelected").show();
        $("#resultButtonSelected").hide();

        $("#proversButtonNotSelected").show();
        $("#vcsButtonNotSelected").hide();
        $("#resultButtonNotSelected").show()();
    });
    $("#Z3ButtonNotSelected").click(function () {
        $.post("/prover", { prover: "Z3" }, function () {
            $("#Z3ButtonSelected").show();
            $("#CVC4ButtonSelected").hide();
            $("#Alt-ErgoButtonSelected").hide();

            $("#Z3ButtonNotSelected").hide();
            $("#CVC4ButtonNotSelected").show();
            $("#Alt-ErgoButtonNotSelected").show();
        });
    });
    $("#CVC4ButtonNotSelected").click(function () {
        $.post("/prover", { prover: "CVC4" }, function () {
            $("#Z3ButtonSelected").hide();
            $("#CVC4ButtonSelected").show();
            $("#Alt-ErgoButtonSelected").hide();

            $("#Z3ButtonNotSelected").show();
            $("#CVC4ButtonNotSelected").hide();
            $("#Alt-ErgoButtonNotSelected").show();
        });
    });
    $("#Alt-ErgoButtonNotSelected").click(function () {
        $.post("/prover", { prover: "Alt-Ergo" }, function () {
            $("#Z3ButtonSelected").hide();
            $("#CVC4ButtonSelected").hide();
            $("#Alt-ErgoButtonSelected").show();

            $("#Z3ButtonNotSelected").show();
            $("#CVC4ButtonNotSelected").show();
            $("#Alt-ErgoButtonNotSelected").hide();
        });
    });
    $("#vcsSubmit").click(function () {
        $.post("/vcs", { vc: $("#vcsInput").val() }, function () { });
    });
    $("#compile").click(function () {
        $.post("/compile", { code: $("#code").val() }, function (data) {
            $("#resultDiv").html(data['result']);
            $("#focus").html(data['focusOnElements']);
        });
    });
    $("#rerunButton").click(function () {
        $.post("/compile", { code: $("#code").val() }, function (data) {
            $("#resultDiv").html(data['result']);
            $("#focus").html(data['focusOnElements']);
        });
    });
    $(".not_selected_button_file_tree").click(function () {
        fileClicked();
    });
    $(".not_selected_button_directory").click(function () {
        directoryClicked();
    });
    $("#nameOfNewDirectory").pressEnter(function () {
        var name = $("#nameOfNewDirectory").val();

        $.post("/newDirectory", { name: name }, function (data) {
            var $newDirectory = $("<button>", {id: data["id"], "class": "not_selected_button_directory"});
            $newDirectory.text(name)
            $newDirectory.click(function () {
                directoryClicked();
            });
            $("#fileTree").append($newDirectory);

            var $newFileForm = $("<input>", {id: "newFile" + data["id"], "class": "selected_button_new_file", "type": "text", "value":"Name of new file" });
            $newFileForm.pressEnter(function () {
                newFileFormPressedEnter();
            });
            $("#fileTree").append($newFileForm);


            $("#nameOfNewDirectory").hide();
        });
    });
    $("#deleteButton").click(function () {
        $.post("/delete", {}, function (data) {
            if (data["whatWasDeleted"] == "file") {
                $("#selectedFile").remove()
                $("#code").val("");
            }
            else
                $("#selectedDirectory").remove()
        });
    });

    if ("{{prover}}" == "CVC4") {
        $("#CVC4ButtonSelected").show();
        $("#CVC4ButtonNotSelected").hide();
    }
    if ("{{prover}}" == "Alt-Ergo") {
        $("#Alt-ErgoButtonSelected").show();
        $("#Alt-ErgoButtonNotSelected").hide();
    }
    if ("{{prover}}" == "Z3") {
        $("#Z3ButtonSelected").show();
        $("#Z3ButtonNotSelected").hide();
    }
    let selectedFile = $("#{{selectedDirectory}}_{{selectedFile}}");
    selectedFile.addClass("selected_button_file_tree");
    selectedFile.removeClass("not_selected_button_file_tree");
    let selectedDirectory = $("#{{selectedDirectory}}");
    selectedDirectory .addClass("selected_button_directory");
    selectedDirectory .removeClass("not_selected_button_directory ");
});