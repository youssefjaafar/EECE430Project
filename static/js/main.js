(function ($) {

    $("#birth_date").datepicker({
        dateFormat: "mm - dd - yy",
        showOn: "both",
        buttonText: '<i class="zmdi zmdi-calendar-alt"></i>',
    });

    $('.add-info-link ').on('click', function () {
        $('.add_info').toggle("slow");
    });

    $('#country').parent().append('<ul class="list-item" id="newcountry" name="country"></ul>');
    $('#country option').each(function () {
        $('#newcountry').append('<li value="' + $(this).val() + '">' + $(this).text() + '</li>');
    });
    $('#country').remove();
    $('#newcountry').attr('id', 'country');
    $('#country li').first().addClass('init');
    $("#country").on("click", ".init", function () {
        $(this).closest("#country").children('li:not(.init)').toggle();
    });

    $('#city').parent().append('<ul class="list-item" id="newcity" name="city"></ul>');
    $('#city option').each(function () {
        $('#newcity').append('<li value="' + $(this).val() + '">' + $(this).text() + '</li>');
    });
    $('#city').remove();
    $('#newcity').attr('id', 'city');
    $('#city li').first().addClass('init');
    $("#city").on("click", ".init", function () {
        $(this).closest("#city").children('li:not(.init)').toggle();
    });

    var allOptions = $("#country").children('li:not(.init)');
    $("#country").on("click", "li:not(.init)", function () {
        allOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#country").children('.init').html($(this).html());
        allOptions.toggle('slow');
    });

    var FoodOptions = $("#city").children('li:not(.init)');
    $("#city").on("click", "li:not(.init)", function () {
        FoodOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#city").children('.init').html($(this).html());
        FoodOptions.toggle('slow');
    });

    $('#signup-form').validate({
        rules: {
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            email: {
                required: true
            },
            password: {
                required: true
            },
            re_password: {
                required: true,
                equalTo: "#password"
            }
        },
        onfocusout: function (element) {
            $(element).valid();
        },
    });

    $('#signin-form').validate({
        rules: {

            email: {
                required: true
            },
            password: {
                required: true
            },

        },
        onfocusout: function (element) {
            $(element).valid();
        },
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });
})(jQuery);