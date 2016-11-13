/*
 *
 *  For User Page
 *  Design By Xiaok
 *  2014-12-10 23:22:54
 *
*/

function add_user() {
    username = $("#username").val();
    name = $("#name").val();
    email = $("#email").val();
    mobile = $("#mobile").val();
    password = $("#password").val();
    password2 = $("#password2").val();
    comment = $("#comment").val();
    if (username == '') {
        alert("{{ _('Please enter a user name') }}");
        $("#username").focus();
        return false;
    };
    if (name == '') {
        alert("{{ _('Please type in your name') }}");
        $("#name").focus();
        return false;
    };
    if (password == '') {
        alert("{{ _('Please enter a password') }}");
        $("#password").focus();
        return false;
    };
    if (password2 == '') {
        alert("{{ _('Please enter the password again') }}");
        $("#password2").focus();
        return false;
    };
    if (password != password2) {
        alert("{{ _('The passwords do not match, please try again') }}");
        $("#password").val("");
        $("#password2").val("");
        $("#password").focus();
        return false;
    };
    $.ajax({
        type: "POST",
        url: "/users",
        data: {
            'username': username,
            'name': name,
            "email": email,
            "mobile": mobile,
            "password": password,
            'comment': comment,
            "fun": "add"
        },
        dataType: "text",
        success: function(msg) {
            if (msg == "1") {
                alert("{{ _('Added successfully') }}");
                window.location.href = "/users";
            } else if (msg == "2") {
                alert("{{ _('User already exists') }}");
                $("#username").focus();
            } else {
                alert("{{ _('Error: Failed to add user') }}");
            }
        },
        error: function() {
            alert("{{ _('Error: Internal Server Error') }}");
        },
    });
};
function show_add() {
    $("#add_line").removeClass("display_no");
    $("#domain").focus();
};
function cancel_add() {
    $("#add_line").addClass("display_no");
};
function to_edit(id) {
    show_id = "#line_" + id;
    edit_id = "#edit_line_" + id;
    $(show_id).addClass("display_no");
    $(edit_id).removeClass("display_no");
};
function to_line(id) {
    show_id = "#line_" + id;
    edit_id = "#edit_line_" + id;
    $(show_id).removeClass("display_no");
    $(edit_id).addClass("display_no");
};

function save_info(id) {
    //username = $("#username_"+id).val();
    name = $("#name_" + id).val();
    email = $("#email_" + id).val();
    mobile = $("#mobile_" + id).val();
    comment = $("#comment_" + id).val();
    $.ajax({
        type: "POST",
        url: "/users",
        data: {
            "id": id,
            "name": name,
            "email": email,
            "mobile": mobile,
            "comment": comment,
            "fun": "edit"
        },
        dataType: "text",
        success: function(msg) {
            if (msg == "1") {
                alert("{{ _('Successfully modified') }}");
                location.href = "/users";
            } else {
                alert("{{ _('Error: Modification failed') }}");
                return false;
            }
        },
        error: function() {
            alert("{{ _('Error: Internal Server Error') }}");
            return false;
        },
    });
};
function ch_pass(id, username) {
    $("#cur_uid").val(id);
    $("#cur_user").val(username);
    $("#oldpass").val("**********");
    $("#userlist").addClass("display_no");
    $("#pass_form").removeClass("display_no");
};
function cancel_pass() {
    $("#pass_form").addClass("display_no");
    $("#userlist").removeClass("display_no");
};
function save_pass() {
    uid = $("#cur_uid").val();
    username = $("#cur_user").val();
    pass1 = $("#newpass").val();
    pass2 = $("#newpass2").val();
    if (pass1 == '' || pass2 == '') {
        alert("{{ _('Error: Password should not be blank') }}");
        $("#newpass").focus();
        return false;
    }
    if (pass1 != pass2) {
        alert("{{ _('Please enter the password twice') }}");
        $("#newpass").val("");
        $("#newpass2").val("");
        $("#newpass").focus();
        return false;
    };
    $.ajax({
        type: "POST",
        url: "/users",
        data: {
            "id": uid,
            "password": pass1,
            "fun": "pass"
        },
        dataType: "text",
        success: function(msg) {
            if (msg == "1") {
                alert("{{ _('The password has been updated successfully') }}");
                location.href = "/users";
            } else {
                alert("{{ _('Error: Failed to update password') }}");
                return false;
            }
        },
        error: function() {
            alert("{{ _('Error: Internal Server Error') }}");
            return false;
        },
    });
};

/*
 *
 *  For User Page
 *  Desgin By Xiaok
 *  2014-12-10 23:22:54
 *
*/
