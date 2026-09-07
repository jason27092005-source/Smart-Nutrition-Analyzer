// ==========================================================
// SMART NUTRITION ANALYZER & DIET RECOMMENDATION SYSTEM
// JavaScript & Chart.js Integration
// ==========================================================

function initDashboardCharts(data) {
    if (!data || !data.categories) {
        console.warn("No chart data available to render.");
        return;
    }

    // Chart 1: Calories by Food Category (Bar Chart)
    const ctxCal = document.getElementById('chartCalories');
    if (ctxCal) {
        new Chart(ctxCal, {
            type: 'bar',
            data: {
                labels: data.categories,
                datasets: [{
                    label: 'Avg Calories (kcal)',
                    data: data.cat_calories,
                    backgroundColor: 'rgba(245, 158, 11, 0.75)',
                    borderColor: 'rgb(217, 119, 6)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Calories (kcal)' }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 20
                        }
                    }
                }
            }
        });
    }

    // Chart 2: Protein Content by Category (Bar Chart)
    const ctxProt = document.getElementById('chartProtein');
    if (ctxProt) {
        new Chart(ctxProt, {
            type: 'bar',
            data: {
                labels: data.categories,
                datasets: [{
                    label: 'Avg Protein (g)',
                    data: data.cat_protein,
                    backgroundColor: 'rgba(46, 125, 50, 0.75)',
                    borderColor: 'rgb(27, 94, 32)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Protein (grams)' }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 20
                        }
                    }
                }
            }
        });
    }

    // Chart 3: Macronutrient Ratio Distribution (Doughnut Chart)
    const ctxMacros = document.getElementById('chartMacros');
    if (ctxMacros) {
        new Chart(ctxMacros, {
            type: 'doughnut',
            data: {
                labels: data.macro_labels,
                datasets: [{
                    data: data.macro_values,
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',  // Carbs - Blue
                        'rgba(46, 125, 50, 0.8)',   // Protein - Green
                        'rgba(245, 158, 11, 0.8)'   // Fat - Amber
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Chart 4: Food Category Distribution (Doughnut Chart)
    const ctxCatDist = document.getElementById('chartCategoryDist');
    if (ctxCatDist) {
        new Chart(ctxCatDist, {
            type: 'doughnut',
            data: {
                labels: data.cat_count_labels,
                datasets: [{
                    data: data.cat_count_values,
                    backgroundColor: [
                        '#2e7d32', '#3b82f6', '#f59e0b', '#ec4899', 
                        '#8b5cf6', '#14b8a6', '#64748b', '#ef4444'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Client-side Input Validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('nutritionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const age = document.getElementById('age');
            const height = document.getElementById('height');
            const weight = document.getElementById('weight');

            if (age && (age.value < 12 || age.value > 100)) {
                alert('Please enter a realistic age between 12 and 100.');
                age.focus();
                e.preventDefault();
                return;
            }
            if (height && (height.value < 90 || height.value > 250)) {
                alert('Please enter a realistic height between 90 and 250 cm.');
                height.focus();
                e.preventDefault();
                return;
            }
            if (weight && (weight.value < 25 || weight.value > 250)) {
                alert('Please enter a realistic weight between 25 and 250 kg.');
                weight.focus();
                e.preventDefault();
                return;
            }
        });
    }
});

