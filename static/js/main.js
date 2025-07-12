$(document).ready(function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').addClass('fade-out');
        setTimeout(function() {
            $('.alert').remove();
        }, 500);
    }, 5000);

    // Confirm delete actions with modern styling
    $('.delete-btn').click(function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    // Enhanced search form validation
    $('#search-form').on('submit', function(e) {
        var query = $('#search-input').val().trim();
        if (query.length < 3) {
            e.preventDefault();
            showToast('Please enter at least 3 characters to search.', 'warning');
        }
    });

    // Scroll to top functionality
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#scrollToTop').addClass('visible');
        } else {
            $('#scrollToTop').removeClass('visible');
        }
    });

    $('#scrollToTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 300);
        return false;
    });

    // Add loading states to buttons
    $('.btn-primary, .btn-success').click(function() {
        var $btn = $(this);
        if ($btn.closest('form').length) {
            setTimeout(function() {
                $btn.prop('disabled', true);
                $btn.html('<span class="loading"></span> Loading...');
            }, 100);
        }
    });

    // Enhanced hover effects
    $('.card').hover(
        function() {
            $(this).addClass('shadow-lg');
        },
        function() {
            $(this).removeClass('shadow-lg');
        }
    );

    // Add smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add animation classes to elements as they come into view
    function animateOnScroll() {
        $('.fade-in-up').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();

            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('animated');
            }
        });
    }

    $(window).on('scroll', animateOnScroll);
    animateOnScroll(); // Run on load
});

// Toast notification function
function showToast(message, type = 'info') {
    const toast = $(`
        <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 1060; min-width: 300px;">
            <i class="fa-solid fa-circle-info me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);

    $('body').append(toast);
    setTimeout(() => toast.remove(), 4000);
}