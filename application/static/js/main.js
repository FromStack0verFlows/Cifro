$(document).ready(function(){
    
    /* Превью документа */
    $(".search.results .res-items .item .controls .download").click(function () {
        var previewDiv = $(this).parents(".item").find('.preview');
        var closeButton = $(this).parents(".item").find('.download');
        if(!closeButton.hasClass('close')){
            closeButton.addClass('close');
        } else {
            closeButton.removeClass('close');
        }
        previewDiv.slideToggle("slow");
    });

    /* Всплывающий фильтр - Mobile */
    $('.search-panel .search-input .settings, .results-bar .filter .action a').click(function(){
        $('.search-settings').addClass('open');
        $('.dark-overlay').addClass('show');
    });
    $('.dark-overlay').click(function(){
        $(this).removeClass('show');
        $('.search-settings').removeClass('open');
        $('.view-detail').removeClass('open');
    });
    $('#open-filters').click(function(){
        if(!$('.search.results .type-menu, .search.results .select-date, .search.results .date-picker').hasClass('open')) {
            $('.search.results .type-menu, .search.results .select-date, .search.results .date-picker').addClass('open');
        } else {
            $('.search.results .type-menu, .search.results .select-date, .search.results .date-picker').removeClass('open');
        }
    });

    /* Смотреть PDF */
    $('.results-bar .filter .action a').click(function(){
        $('.view-detail').addClass('open');
        $('.dark-overlay').addClass('show');
    });
    $('.view-detail .controls .close').click(function(){
        $('.dark-overlay').removeClass('show');
        $('.view-detail').removeClass('open');
    });

    /* Меню выбора категорий */
    const typeChoiceButton = $('#type-choice'),
    typeMenuPanel = $('.search-panel .doc-types .type-menu');
    typeChoiceButton.click(function(){
        if(!typeMenuPanel.hasClass('open')) {
            typeMenuPanel.addClass('open');
        } else {
            typeMenuPanel.removeClass('open');
        }
    });
    $(document).click(function (e) {
        if ( !typeChoiceButton.is(e.target) && !typeMenuPanel.is(e.target) && typeMenuPanel.has(e.target).length === 0) {
            if(typeMenuPanel.hasClass('open')) {    
                typeMenuPanel.removeClass('open');
            }
        };
    });

    $(document).on('click', '.search-panel .doc-types .type-menu ul li label, .search.results .type-menu ul li input+label', function(){
        var catTitle = $(this).text(),
        catVal = $(this).attr('for'),
        countChecked = $(".search-panel .doc-types .type-menu ul li input:checked").length;
        $('.search-panel .search-input .categories .close-all').remove();
        if($('#'+catVal).is(":checked")) {
            $('.search-panel .search-input .categories').find("[data-cat='" + catVal + "']").remove();
            countChecked = countChecked - 1;
        } else {
            $('.search-panel .search-input .categories').append('<a href="javascript:void(0);" class="cat" data-cat="'+ catVal +'">'+ catTitle +'</a>');
            $('.search-panel .search-input .categories').append('<a href="javascript:void(0);" class="close-all">Сбросить</a>');
            countChecked = countChecked + 1;
        }
        if($('#type-choice').length){
            if (countChecked == 0) {
                $('#type-choice').text('Все документы');
            } else {
                $('#type-choice').text('Категории (' + countChecked + ')');
            }
        } 
    });

    $(document).on('click','.search-panel .search-input .categories a', function(){
        var catProp = $(this).attr('data-cat');
        $('.search.results .type-menu ul li #' + catProp).prop('checked',false);
        $('.search-panel .doc-types .type-menu ul li #' + catProp).prop('checked',false);
        countChecked = $(".search-panel .doc-types .type-menu ul li input:checked").length;
        $(this).remove();
        if($('.search-panel .search-input .categories a').length == 1) {
            $('.search-panel .search-input .categories a').remove();
        }
        if($('#type-choice').length && $('.search-panel .search-input .categories a').length == 0){ 
            $('#type-choice').text('Все документы');
        } else {
            $('#type-choice').text('Категории (' + countChecked + ')');
        }
    });

    $(document).on('click','.close-all', function(){
        $('.search.results .type-menu ul li input').prop('checked',false);
        $('#type-choice').text('Все документы');
    });

    $(document).on('click','.search-panel .search-input .categories .close-all',function(){
        $('.search-panel .search-input .categories a').remove();
        $('.search-panel .doc-types .type-menu ul li input').prop('checked', false);
    });

    /* Календарь */
    $('#date-picker-show').datepicker({
        dateFormat : "yy-mm-dd",
        range: 'period', // режим - выбор периода
        numberOfMonths: 1,
        onSelect: function(dateText, inst, extensionRange) {
            // extensionRange - объект расширения
            $('[name=startDate]').val(extensionRange.startDateText);
            $('[name=endDate]').val(extensionRange.endDateText);
            if(extensionRange.startDateText == extensionRange.endDateText) {
                $('.search.results .select-date .dp').text(extensionRange.startDateText);
            } else {
                $('.search.results .select-date .dp').text('с ' + extensionRange.startDateText + ' по ' + extensionRange.endDateText);
            }
        },
        monthNames : ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        dayNamesMin : ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'],
    });
    
    $('#date-picker-show').datepicker('setDate', ['0d']);
    
    // объект расширения (хранит состояние календаря)
    var extensionRange = $('#date-picker-show').datepicker('widget').data('datepickerExtensionRange');
    if(extensionRange.startDateText) { $('[name=startDate]').val(extensionRange.startDateText); }
    if(extensionRange.endDateText) { $('[name=endDate]').val(extensionRange.endDateText);}

    const dateChoiceButton = $('#date-choice'),
    datepickerPanel = $('.search .search-panel .date .datepicker');
    datePickerArrowNext = $('.ui-datepicker-header');
    dateChoiceButton.click(function(){
        if(!datepickerPanel.hasClass('open')) {
            datepickerPanel.addClass('open');
        } else {
            datepickerPanel.removeClass('open');
        }
    });
    $(document).click(function (e) {
            if ( !dateChoiceButton.is(e.target) && !datepickerPanel.is(e.target) && datepickerPanel.has(e.target).length === 0) {
                if(datepickerPanel.hasClass('open')) {    
                    datepickerPanel.removeClass('open');
                }
            };
    });
});
  