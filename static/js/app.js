// GeneXium Training Plan Generator - Frontend JavaScript



// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up form submission
    const form = document.getElementById('trainingPlanForm');
    form.addEventListener('submit', handleFormSubmission);

    // Set up daily workout form submission
    const dailyWorkoutForm = document.getElementById('dailyWorkoutForm');
    dailyWorkoutForm.addEventListener('submit', handleDailyWorkoutSubmission);

    // Initialize marked.js for markdown rendering
    marked.setOptions({
        breaks: true,
        gfm: true
    });
}



async function handleFormSubmission(event) {
    event.preventDefault();
    
    const geneSelect = document.getElementById('geneSelect');
    const goalInput = document.getElementById('goalInput');
    const generateBtn = document.getElementById('generateBtn');
    
    const gene = geneSelect.value;
    const goal = goalInput.value.trim();
    
    if (!gene || !goal) {
        showError('Please select a gene and enter your fitness goal.');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch('/generate_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gene: gene,
                goal: goal
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showResults(data);
        } else {
            showError(data.error || 'An error occurred while generating your training plan.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

function showLoading() {
    // Hide other sections
    document.getElementById('emptyState').classList.add('d-none');
    document.getElementById('errorSection').classList.add('d-none');
    document.getElementById('resultsSection').classList.add('d-none');
    
    // Show loading section
    document.getElementById('loadingSection').classList.remove('d-none');
    
    // Disable form
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('generateBtn').innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
}

function showError(message) {
    // Hide other sections
    document.getElementById('loadingSection').classList.add('d-none');
    document.getElementById('emptyState').classList.add('d-none');
    document.getElementById('resultsSection').classList.add('d-none');
    
    // Show error section
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').classList.remove('d-none');
    
    // Re-enable form
    document.getElementById('generateBtn').disabled = false;
    document.getElementById('generateBtn').innerHTML = '<i class="fas fa-magic me-2"></i>Generate Training Plan';
}

function showResults(data) {
    // Hide other sections
    document.getElementById('loadingSection').classList.add('d-none');
    document.getElementById('errorSection').classList.add('d-none');
    document.getElementById('emptyState').classList.add('d-none');
    
    // Show results section
    document.getElementById('selectedGene').textContent = data.gene.toUpperCase();
    
    // Render training plan content
    const trainingPlanContent = document.getElementById('trainingPlanContent');
    trainingPlanContent.innerHTML = marked.parse(data.training_plan);
    trainingPlanContent.classList.add('fade-in');
    
    // Render research report content
    const researchReportContent = document.getElementById('researchReportContent');
    researchReportContent.innerHTML = marked.parse(data.research_report);
    researchReportContent.classList.add('fade-in');
    
    document.getElementById('resultsSection').classList.remove('d-none');
    
    // Re-enable form
    document.getElementById('generateBtn').disabled = false;
    document.getElementById('generateBtn').innerHTML = '<i class="fas fa-magic me-2"></i>Generate Training Plan';
    
    // Show daily workout form
    document.getElementById('dailyWorkoutCard').style.display = 'block';
    
    // Store training plan data for daily workout generation
    window.currentTrainingPlan = data.training_plan;
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

async function handleDailyWorkoutSubmission(event) {
    event.preventDefault();
    
    const weekNumber = document.getElementById('weekNumber').value;
    const dayOfWeek = document.getElementById('dayOfWeek').value;
    const hrv = document.getElementById('hrv').value;
    const restingHeartRate = document.getElementById('restingHeartRate').value;
    const hoursOfSleep = document.getElementById('hoursOfSleep').value;
    const generateWorkoutBtn = document.getElementById('generateWorkoutBtn');
    
    if (!weekNumber || !dayOfWeek) {
        showError('Please select both week number and day of week.');
        return;
    }
    
    if (!window.currentTrainingPlan) {
        showError('Please generate a training plan first.');
        return;
    }
    
    // Show loading state for workout generation
    generateWorkoutBtn.disabled = true;
    generateWorkoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
    
    try {
        const response = await fetch('/generate_daily_workout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                training_plan: window.currentTrainingPlan,
                week_number: weekNumber,
                day_of_week: dayOfWeek,
                hrv: hrv || null,
                resting_heart_rate: restingHeartRate || null,
                hours_of_sleep: hoursOfSleep || null
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showDailyWorkoutResults(data.daily_workout, weekNumber, dayOfWeek);
        } else {
            showError(data.error || 'An error occurred while generating your daily workout.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        // Re-enable button
        generateWorkoutBtn.disabled = false;
        generateWorkoutBtn.innerHTML = '<i class="fas fa-dumbbell me-2"></i>Generate Daily Workout';
    }
}

function showDailyWorkoutResults(dailyWorkout, weekNumber, dayOfWeek) {
    // Render daily workout content
    const dailyWorkoutContent = document.getElementById('dailyWorkoutContent');
    dailyWorkoutContent.innerHTML = marked.parse(dailyWorkout);
    dailyWorkoutContent.classList.add('fade-in');
    
    // Switch to daily workout tab
    const dailyWorkoutTab = document.getElementById('daily-workout-tab');
    const tab = new bootstrap.Tab(dailyWorkoutTab);
    tab.show();
    
    // Show success notification
    showNotification(`Daily workout generated for Week ${weekNumber}, ${dayOfWeek}!`, 'success');
}

function downloadPlan() {
    const gene = document.getElementById('selectedGene').textContent;
    
    // Get the currently active tab
    const activeTab = document.querySelector('#resultsTabs .nav-link.active');
    const isTrainingActive = activeTab.id === 'training-tab';
    const isResearchActive = activeTab.id === 'research-tab';
    const isDailyWorkoutActive = activeTab.id === 'daily-workout-tab';
    
    // Get the appropriate content
    let contentElement;
    if (isTrainingActive) {
        contentElement = document.getElementById('trainingPlanContent');
    } else if (isResearchActive) {
        contentElement = document.getElementById('researchReportContent');
    } else if (isDailyWorkoutActive) {
        contentElement = document.getElementById('dailyWorkoutContent');
    }
    
    // Create a temporary element to get the text content
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = contentElement.innerHTML;
    
    // Convert HTML back to markdown (simplified)
    let markdownText = '';
    
    // Add header based on content type
    let contentType;
    if (isTrainingActive) {
        contentType = 'Training Plan';
    } else if (isResearchActive) {
        contentType = 'Research Report';
    } else if (isDailyWorkoutActive) {
        contentType = 'Daily Workout';
    }
    markdownText += `# ${gene} ${contentType}\n\n`;
    
    // Convert content
    const elements = tempDiv.children;
    for (let element of elements) {
        if (element.tagName === 'H1') {
            markdownText += `# ${element.textContent}\n\n`;
        } else if (element.tagName === 'H2') {
            markdownText += `## ${element.textContent}\n\n`;
        } else if (element.tagName === 'H3') {
            markdownText += `### ${element.textContent}\n\n`;
        } else if (element.tagName === 'H4') {
            markdownText += `#### ${element.textContent}\n\n`;
        } else if (element.tagName === 'P') {
            markdownText += `${element.textContent}\n\n`;
        } else if (element.tagName === 'UL') {
            const items = element.querySelectorAll('li');
            for (let item of items) {
                markdownText += `- ${item.textContent}\n`;
            }
            markdownText += '\n';
        } else if (element.tagName === 'OL') {
            const items = element.querySelectorAll('li');
            for (let i = 0; i < items.length; i++) {
                markdownText += `${i + 1}. ${items[i].textContent}\n`;
            }
            markdownText += '\n';
        } else if (element.tagName === 'BLOCKQUOTE') {
            markdownText += `> ${element.textContent}\n\n`;
        }
    }
    
    // Create and download file
    let fileName;
    if (isTrainingActive) {
        fileName = `${gene.toLowerCase()}_training_plan.md`;
    } else if (isResearchActive) {
        fileName = `${gene.toLowerCase()}_research_report.md`;
    } else if (isDailyWorkoutActive) {
        fileName = `${gene.toLowerCase()}_daily_workout.md`;
    }
    
    const blob = new Blob([markdownText], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Add some utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
} 