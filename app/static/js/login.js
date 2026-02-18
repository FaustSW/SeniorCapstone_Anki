        /* ============================================================================================================== */
        /* STORE ALL PROFILES */
        /* ============================================================================================================== */
        
        let profiles = [
            { id: 1, name: 'John Doe', username: 'john_doe', password: 'password123', avatar: 'avatar-1', initials: 'JD' },
            { id: 2, name: 'Jane Smith', username: 'jane_smith', password: 'secure456', avatar: 'avatar-2', initials: 'JS' },
            { id: 3, name: 'Admin', username: 'admin', password: 'admin789', avatar: 'avatar-3', initials: 'AD' },
            { id: 4, name: 'Demo User', username: 'demo_user', password: 'demo2024', avatar: 'avatar-4', initials: 'DU' }
        ];

        let selectedProfile = null;


        /* ============================================================================================================== */
        /* LOAD AND SAVE PROFILES */
        /* ============================================================================================================== */
        
        function loadProfiles() {
            const saved = localStorage.getItem('profiles');
            if (saved) {
                profiles = JSON.parse(saved);
            }
            renderProfiles();
        }

        function saveProfiles() {
            localStorage.setItem('profiles', JSON.stringify(profiles));
        }


        /* ============================================================================================================== */
        /* DISPLAY ALL PROFILE CARDS */
        /* ============================================================================================================== */
        
        function renderProfiles() {
            const grid = document.getElementById('profilesGrid');
            grid.innerHTML = ''; // Clear old profiles first

            
            profiles.forEach(profile => {
                const profileCard = document.createElement('div');
                profileCard.className = 'profile-card';
                profileCard.onclick = () => selectProfile(profile);

                profileCard.innerHTML = `
                    <button class="remove-btn" onclick="removeProfile(event, ${profile.id})">×</button>
                    <div class="profile-avatar ${profile.avatar}">${profile.initials}</div>
                    <div class="profile-name">${profile.name}</div>
                    <div class="profile-username">@${profile.username}</div>
                `;

                grid.appendChild(profileCard);
            });
        }


        /* ============================================================================================================== */
        /* PROFILE CLICK */
        /* ============================================================================================================== */
        
        function selectProfile(profile) {
            selectedProfile = profile;
            
            
            document.querySelectorAll('.profile-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            event.currentTarget.classList.add('selected');
            document.getElementById('selectedProfileName').textContent = `Enter password for ${profile.name}`;
            document.getElementById('passwordSection').style.display = 'block';
            document.getElementById('passwordInput').value = '';
            document.getElementById('passwordInput').focus();
            document.getElementById('message').style.display = 'none';
            document.getElementById('passwordError').classList.remove('show');
        }


        /* ============================================================================================================== */
        /* REMOVE PROFILE */
        /* ============================================================================================================== */
        
        function removeProfile(event, profileId) {
            
            event.stopPropagation();

            
            const profile = profiles.find(p => p.id === profileId);
            if (confirm(`Are you sure you want to delete ${profile.name}?`)) {
                profiles = profiles.filter(p => p.id !== profileId);
                saveProfiles();
                renderProfiles();
                selectedProfile = null;
                document.getElementById('passwordSection').style.display = 'none';
                document.getElementById('selectedProfileName').textContent = 'Select a profile to continue';
                document.getElementById('message').style.display = 'none';
                
                showMessage(`✅ ${profile.name} has been deleted!`, 'success');
            }
        }


        /* ============================================================================================================== */
        /* CHECK PASSWORD & LOGIN */
        /* ============================================================================================================== */
        
        function handleLogin() {
            if (!selectedProfile) {
                showMessage('Please select a profile', 'error');
                return;
            }

            const password = document.getElementById('passwordInput').value;

            // Check if password matches
            if (password === selectedProfile.password) {

                // Password is CORRECT
                document.getElementById('passwordError').classList.remove('show');
                showMessage(`✅ Welcome, ${selectedProfile.name}!`, 'success');
                setTimeout(() => {
                    alert(`Successfully logged in as ${selectedProfile.name}!`);
                }, 500);

                fetch('/card', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/card';
                    } else {
                        showMessage('Error navigating to card page', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error navigating to card page', 'error');
                });
            }
            
            else {
                // Password is WRONG
                document.getElementById('passwordError').classList.add('show');
                document.getElementById('passwordInput').value = '';
                document.getElementById('passwordInput').focus();
            }
        }

        
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = text;
            messageDiv.className = `message ${type}`;
        }


        /* ============================================================================================================== */
        /* OPEN/CLOSE POP UP (add profile pop up) */
        /* ============================================================================================================== */
        
        function openAddProfileModal() {
            document.getElementById('addProfileModal').classList.add('show');
        }

        
        function closeAddProfileModal() {
            document.getElementById('addProfileModal').classList.remove('show');
            document.getElementById('createProfileForm').reset();
        }


        /* ============================================================================================================== */
        /* CREATE NEW PROFILE */
        /* ============================================================================================================== */
       
        document.getElementById('createProfileForm').addEventListener('submit', function(e) {
            e.preventDefault();

            
            const name = document.getElementById('newUsername').value;
            const username = document.getElementById('newLoginUsername').value;
            const password = document.getElementById('newPassword').value;

            
            if (profiles.find(p => p.username === username)) {
                alert('Username already exists!');
                return;
            }

            
            const initials = name.split(' ').map(word => word[0]).join('').toUpperCase();
            const avatarClass = `avatar-${(profiles.length % 5) + 1}`;

            profiles.push({
                id: profiles.length + 1,
                name: name,
                username: username,
                password: password,
                avatar: avatarClass,
                initials: initials
            });

            
            saveProfiles();
            renderProfiles();
            closeAddProfileModal();
            showMessage('✅ Profile created successfully!', 'success');
        });


        /* ============================================================================================================== */
        /* EXTRA - for extra functions */
        /* ============================================================================================================== */
        
        // Close pop-up when clicking outside of it
        window.onclick = function(event) {
            const modal = document.getElementById('addProfileModal');
            if (event.target === modal) {
                closeAddProfileModal();
            }
        }

        // Press Enter key to login instead of clicking button
        document.getElementById('passwordInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleLogin();
            }
        });

        // Load all profiles when page first opens
        loadProfiles();