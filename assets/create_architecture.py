# Architecture Diagram Generator
# This script creates the system architecture visualization

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Define colors
primary_blue = '#1f77b4'
secondary_green = '#2ca02c'
accent_orange = '#ff7f0e'
light_gray = '#f0f0f0'
dark_gray = '#404040'

# Title
ax.text(5, 7.5, 'Telco Churn Prediction System Architecture', 
        fontsize=18, fontweight='bold', ha='center')

# Data Sources Layer
data_box = FancyBboxPatch((0.5, 6), 3, 1, boxstyle="round,pad=0.1", 
                          facecolor=light_gray, edgecolor=dark_gray, linewidth=2)
ax.add_patch(data_box)
ax.text(2, 6.5, 'DATA SOURCES', fontsize=12, fontweight='bold', ha='center')
ax.text(0.7, 6.3, '• Customer Database', fontsize=9, ha='left')
ax.text(0.7, 6.1, '• Billing System', fontsize=9, ha='left')
ax.text(2.2, 6.3, '• Service Usage Logs', fontsize=9, ha='left')
ax.text(2.2, 6.1, '• Support Interactions', fontsize=9, ha='left')

# ML Pipeline Layer
ml_box = FancyBboxPatch((4.5, 6), 4.5, 1, boxstyle="round,pad=0.1", 
                        facecolor='#e3f2fd', edgecolor=primary_blue, linewidth=2)
ax.add_patch(ml_box)
ax.text(6.75, 6.5, 'ML PIPELINE', fontsize=12, fontweight='bold', ha='center')
ax.text(4.7, 6.3, '• Data Preprocessing', fontsize=9, ha='left')
ax.text(4.7, 6.1, '• Feature Engineering', fontsize=9, ha='left')
ax.text(6.8, 6.3, '• Model Training', fontsize=9, ha='left')
ax.text(6.8, 6.1, '• Logistic Regression', fontsize=9, ha='left')

# Production System Layer
# Backend
backend_box = FancyBboxPatch((0.5, 4), 2, 1.5, boxstyle="round,pad=0.1", 
                            facecolor='#f3e5f5', edgecolor='#9c27b0', linewidth=2)
ax.add_patch(backend_box)
ax.text(1.5, 5, 'BACKEND API', fontsize=11, fontweight='bold', ha='center')
ax.text(1.5, 4.7, 'FastAPI', fontsize=10, ha='center')
ax.text(1.5, 4.5, 'Port 8081', fontsize=9, ha='center')
ax.text(1.5, 4.3, '• Prediction Endpoint', fontsize=8, ha='center')
ax.text(1.5, 4.1, '• Model Serving', fontsize=8, ha='center')

# Frontend
frontend_box = FancyBboxPatch((3, 4), 2, 1.5, boxstyle="round,pad=0.1", 
                             facecolor='#e8f5e8', edgecolor=secondary_green, linewidth=2)
ax.add_patch(frontend_box)
ax.text(4, 5, 'FRONTEND UI', fontsize=11, fontweight='bold', ha='center')
ax.text(4, 4.7, 'Streamlit', fontsize=10, ha='center')
ax.text(4, 4.5, 'Port 8501', fontsize=9, ha='center')
ax.text(4, 4.3, '• Interactive Dashboard', fontsize=8, ha='center')
ax.text(4, 4.1, '• Real-time Predictions', fontsize=8, ha='center')

# Model Storage
storage_box = FancyBboxPatch((5.5, 4), 2, 1.5, boxstyle="round,pad=0.1", 
                            facecolor='#fff3e0', edgecolor=accent_orange, linewidth=2)
ax.add_patch(storage_box)
ax.text(6.5, 5, 'MODEL STORAGE', fontsize=11, fontweight='bold', ha='center')
ax.text(6.5, 4.7, 'Pickle Files', fontsize=10, ha='center')
ax.text(6.5, 4.5, '• Model.pkl', fontsize=8, ha='center')
ax.text(6.5, 4.3, '• Scaler.pkl', fontsize=8, ha='center')
ax.text(6.5, 4.1, '• Encoders.pkl', fontsize=8, ha='center')

# Deployment Layer
deploy_box = FancyBboxPatch((1, 2), 7, 1, boxstyle="round,pad=0.1", 
                           facecolor='#fff8e1', edgecolor='#f57c00', linewidth=2)
ax.add_patch(deploy_box)
ax.text(4.5, 2.5, 'DEPLOYMENT & INFRASTRUCTURE', fontsize=12, fontweight='bold', ha='center')
ax.text(1.5, 2.2, '• Docker Containers', fontsize=9, ha='left')
ax.text(3.5, 2.2, '• AWS App Runner', fontsize=9, ha='left')
ax.text(5.5, 2.2, '• Auto Scaling', fontsize=9, ha='left')
ax.text(7, 2.2, '• Load Balancer', fontsize=9, ha='left')

# Users
users_box = FancyBboxPatch((3.5, 0.5), 2.5, 0.8, boxstyle="round,pad=0.1", 
                          facecolor='#e1f5fe', edgecolor=primary_blue, linewidth=2)
ax.add_patch(users_box)
ax.text(4.75, 0.9, 'BUSINESS USERS', fontsize=11, fontweight='bold', ha='center')
ax.text(4.75, 0.6, 'Customer Success Teams', fontsize=9, ha='center')

# Arrows
# Data flow arrows
ax.arrow(2, 6, 2.3, 0, head_width=0.1, head_length=0.1, fc=dark_gray, ec=dark_gray)
ax.arrow(6.75, 6, 0, -0.3, head_width=0.1, head_length=0.1, fc=dark_gray, ec=dark_gray)
ax.arrow(6.5, 4, -4, 0, head_width=0.1, head_length=0.1, fc=dark_gray, ec=dark_gray)
ax.arrow(4, 4, 0, -1.3, head_width=0.1, head_length=0.1, fc=dark_gray, ec=dark_gray)
ax.arrow(4.75, 1.3, 0, -0.4, head_width=0.1, head_length=0.1, fc=dark_gray, ec=dark_gray)

# Performance metrics box
perf_box = FancyBboxPatch((8.2, 4.5), 1.5, 2.5, boxstyle="round,pad=0.1", 
                         facecolor='#f1f8e9', edgecolor=secondary_green, linewidth=2)
ax.add_patch(perf_box)
ax.text(8.95, 6.7, 'PERFORMANCE', fontsize=10, fontweight='bold', ha='center')
ax.text(8.95, 6.4, 'Recall: 91.7%', fontsize=9, ha='center', color=secondary_green, fontweight='bold')
ax.text(8.95, 6.1, 'ROI: 604.5%', fontsize=9, ha='center', color=secondary_green, fontweight='bold')
ax.text(8.95, 5.8, 'Latency: <200ms', fontsize=8, ha='center')
ax.text(8.95, 5.5, 'Uptime: 99.9%', fontsize=8, ha='center')
ax.text(8.95, 5.2, 'Throughput:', fontsize=8, ha='center')
ax.text(8.95, 4.9, '100K+ pred/hr', fontsize=8, ha='center')

plt.tight_layout()
plt.savefig('c:/Users/heito/Desktop/projects/personal/telco-customer-churn/assets/system_architecture.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("✅ System architecture diagram created!")