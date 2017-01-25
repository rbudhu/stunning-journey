var urls = urls || {};

urls.share_tenso = function() {
    var url = "{% url 'web:share_tenso' %}";
    return url;
};
