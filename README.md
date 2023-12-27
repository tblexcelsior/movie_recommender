# HOW TO RUN:
## NOTE: Since several libraries cannot be installed on Window, so please run this on WSL or Ubuntu.

### Step 1: Setup Database
<p>Download database from this <a href="https://drive.google.com/file/d/1r36hKswbGBLTJzjZU0oGreaKkUsi4_gC/view?usp=sharing">link</a></p>
<p>Create database by <code>CREATE DATABASE recommender;</code></p>
<p>Import downloaded database by <code>mysql -u your_user_name -p recommender < recommender.sql</code></p>

### Step 2: Download models
<p>Download models from this <a href="https://drive.google.com/file/d/18pvYdNX90pttxofKLK3yfb_xqb8ThY7p/view?usp=sharing">link</a></p>
<p>Unrar model.rar and move 'model' folder inside 'ml' folder</p>

### Step 3: Install requirements
<p><code>conda create --name recommender python=3.9.18</code></p>
<p><code>conda activate recommender</code></p>
<p><code>pip install -r ml/requirements.txt</code></p>

### Run
<p>In ml/utils/connector.py, please replace hostname, username, password in line 5, 6, 7 with your MySQL server credentials</p>
<p>Open a terminal and run <code>python ml/api/server.py</code></p>
<p>Open another terminal and run <code>streamlit run demo/app.py</code></p>
<p>Open http://localhost:8501 and start testing</p>
