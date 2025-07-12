$(document).ready(function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm delete actions
    $('.delete-btn').click(function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    // Search form enhancements
    $('#search-form').on('submit', function(e) {
        var query = $('#search-input').val().trim();
        if (query.length < 3) {
            e.preventDefault();
            alert('Please enter at least 3 characters to search.');
        }
    });
});