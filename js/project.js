/**
 * Author: cloudbeer (cloudbeer@gmail.com)
 * Date: 13-4-1
 * Time: 上午9:52
 * GNU license.
 */

$(function () {
    var act = 'create';
    var ref_name = '';
    var table_name = '';

    var v_project = $("#form_project").validate({
        rules: {
            p_title: "required"
        }
    });

    var v_table = $("#form_table").validate({
        rules: {
            t_title: "required",
            t_name: 'required'
        }
    });

    var v_col = $("#form_col").validate({
        rules: {
            c_title: "required",
            c_name: 'required'
        }
    });

    function reset_form() {
        $("#t_name").val("");
        $("#t_title").val("");
        $("#t_content").val("");
    }

    $("#btn_save_project").click(function () {
        if (!$("#form_project").valid()) return;
        var xtitle = $("#p_title").val();
        var db = $("#p_db").val();
        $.post("/project/save/", {title: xtitle, content: $("#p_content").val(), db: db}, function (res) {
            if (res.state) {
                $("#l_project").html(xtitle);
                $(".edit_div").hide();
                $.post("/project/sql_types/", {db: db}, function (res) {
                    if (res.state) {
                        $("#c_type").html("");
                        var sql_types = res.sql_types;
                        for (var i = 0; i < sql_types.length; i++) {
                            $("#c_type").append("<option value='" + sql_types[i] + "'>" + sql_types[i] + "</option>");
                            //console.log(sql_types[i]);
                        }
                        return;
                    }
                    alert(res.message);
                }, 'json');
                return;
            }
            alert(res.message);
        }, 'json');
    });

    $("#edit_project").on('click', function () {
        $.post("/project/get_project/", {}, function (res) {
            if (res.state) {
                $("#p_title").val(res.title);
                $("#p_content").val(res.content);
                $("#p_db").val(res.db);
                $(".edit_div").hide();
                $("#d_create_project").show();
            }
        }, 'json');
    });

    $("#add_table").on('click', function () {
        $(".edit_div").hide();
        reset_form();
        act = "create";
        $("#d_create_table").show()
    });

    $("#btn_save_table").click(function () {
        if (!$("#form_table").valid()) return;
        var xtitle = $("#t_title").val();
        var xname = $("#t_name").val();

        $.post("/project/save_table/",
            {act: act, ref_name: ref_name, title: xtitle, name: xname, content: $("#t_content").val()},
            function (res) {
                if (res.state) {
                    //$("#l_project").html("[P] " + xtitle);
                    $(".edit_div").hide();
                    if (act == "create") {
                        $("#accordion_project").append('<div class="accordion-group" data-flag="' + xname + '"> \
                                            <div class="accordion-heading" style="position: relative"> \
                                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion_project" \
                                    href="#tb_' + xname + '"> \
                                            <i class="icon-calendar"></i> <span class="l_t_name">' + xtitle + ' [' + xname + ']</span> \
                                            </a> \
                                            <span class="btn-group table-button" style="position: absolute;top: 5px;right: 10px"> \
                                            <button class="btn btn-small btn-success add_col"><i class="icon-plus icon-white"></i></button> \
                                    <button class="btn btn-small btn-success edit_table"><i class="icon-edit icon-white"></i> \
                                            </button> \
                                            </span> \
                                            </div> \
                                            <div id="tb_' + xname + '" class="accordion-body collapse"> \
                                            <div class="accordion-inner"> \
                                            </div> \
                                            </div> \
                                            </div>');
                    } else if (act == "modi") {
                        //todo....
                        $(".accordion-group[data-flag='" + ref_name + "'] .l_t_name").html(xtitle + " [" + xname + "]");
                        $(".accordion-group[data-flag='" + ref_name + "']").attr("data-flag", xname);
                    }
                    return;
                }
                $("#pg_error_table").html(res.message);
            }, 'json');
    });

    $(".edit_table").on('click', function () {
        var flag = $(this).parent().parent().parent().attr("data-flag");
        $.post("/project/get_table/", {flag: flag}, function (res) {
            if (res.state) {
                ref_name = res.name;
                act = "modi";
                //console.log(res);
                $("#t_name").val(res.name);
                $("#t_title").val(res.title);
                $("#t_content").val(res.content);
                $(".edit_div").hide();
                $("#d_create_table").show();
            }
        }, 'json');
    });

    $(".add_col").on('click', function () {
        $(".edit_div").hide();
        reset_form();
        act = "create";
        table_name = $(this).parent().parent().parent().attr("data-flag");
        $("#d_create_col").show()
    });


    $("#btn_save_col").click(function () {
        if (!$("#form_col").valid()) return;
        var xtitle = $("#c_title").val();
        var xname = $("#c_name").val();

        $.post("/project/save_col/",
            {act: act, ref_name: ref_name, title: xtitle, name: xname, content: $("#c_content").val(), table: table_name,
                sql_type: $("#c_type").val(), is_pk: $("#is_pk").prop("checked"), is_null: $("#is_null").prop("checked"),
                is_unique: $("#is_unique").prop("checked"), is_index: $("#is_index").prop("checked"),
                auto_incres: $("#auto_incres").prop("checked"), init_val: $("#c_init_val").val()},
            function (res) {
                if (res.state) {
                    //$("#l_project").html("[P] " + xtitle);
                    $(".edit_div").hide();
                    if (act == "create") {
                        $("#tb_" + table_name + " .accordion-inner").append('\
                            <div class="xcol" data-flag="' + xname + '">\
                                <i class="icon-leaf"></i> ' + xtitle + ' [' + xname + ']\
                                <span class="btn-group table-button pull-right">\
                                    <button class="btn btn-small btn-danger del_col">\
                            <i class="icon-remove icon-white"></i></button>\
                                    <button class="btn btn-small btn-success edit_col">\
                                        <i class="icon-edit icon-white"></i>\
                                    </button>\
                                </span>\
                            </div>\
                        '
                        );
                    } else if (act == "modi") {
                        //todo....
                        //$(".accordion-group[data-flag='" + ref_name + "'] .l_t_name").html(xtitle + " [" + xname + "]");
                        //$(".accordion-group[data-flag='" + ref_name + "']").attr("data-flag", xname);
                    }
                    return;
                }
                $("#pg_error_col").html(res.message);
            }, 'json');
    });

    $(".save_project").click(function () {
        $.post("/project/save2db/", {}, function () {
            alert(0);
        });
    });

//    $("#c_db").change(function () {
//        $.post("/project/sql_types/", {db: $(this).val()}, function (res) {
//            if (res.state) {
//
//                return;
//            }
//            alert(res.message);
//        }, 'json');
//    });

});