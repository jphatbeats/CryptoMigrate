/**
 * Animated Market Trend Prediction Widget
 * Provides real-time market predictions with visual animations
 */

class MarketPredictionWidget {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            updateInterval: 30000, // 30 seconds
            symbols: ['BTC', 'ETH', 'XRP', 'ADA', 'SOL'],
            timeframes: ['1h', '4h', '1d', '7d'],
            apiEndpoint: '/api/ai/market-predictions',
            ...options
        };
        
        this.currentSymbol = this.options.symbols[0];
        this.currentTimeframe = '1d';
        this.predictions = {};
        this.chart = null;
        this.isLoading = false;
        this.confidence = 0;
        
        this.init();
    }
    
    init() {
        this.render();
        this.initChart();
        this.bindEvents();
        this.startUpdates();
        this.loadPredictions();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="market-trend-widget fade-in">
                <div class="widget-header">
                    <h3 class="widget-title">
                        <span class="pulse-dot"></span>
                        AI Market Predictions
                    </h3>
                    <div class="prediction-status">
                        <span class="status-indicator">●</span>
                        <span id="prediction-status-text">Analyzing...</span>
                    </div>
                </div>
                
                <div class="symbol-selector">
                    <div class="selector-buttons">
                        ${this.options.symbols.map(symbol => 
                            `<button class="symbol-btn ${symbol === this.currentSymbol ? 'active' : ''}" 
                                     data-symbol="${symbol}">${symbol}</button>`
                        ).join('')}
                    </div>
                    <div class="timeframe-selector">
                        ${this.options.timeframes.map(tf => 
                            `<button class="timeframe-btn ${tf === this.currentTimeframe ? 'active' : ''}" 
                                     data-timeframe="${tf}">${tf}</button>`
                        ).join('')}
                    </div>
                </div>
                
                <div class="prediction-container">
                    <div class="prediction-metrics">
                        <div class="metric-card slide-up">
                            <div class="metric-label">Price Target</div>
                            <div class="metric-value" id="price-target">--</div>
                            <div class="metric-trend" id="price-trend">
                                <span>Calculating...</span>
                            </div>
                        </div>
                        
                        <div class="metric-card slide-up">
                            <div class="metric-label">Probability</div>
                            <div class="metric-value" id="prediction-probability">--%</div>
                            <div class="metric-trend" id="probability-trend">
                                <span>AI Analysis</span>
                            </div>
                        </div>
                        
                        <div class="metric-card slide-up">
                            <div class="metric-label">Time Target</div>
                            <div class="metric-value" id="time-target">--</div>
                            <div class="metric-trend" id="time-trend">
                                <span>Estimation</span>
                            </div>
                        </div>
                        
                        <div class="metric-card slide-up">
                            <div class="metric-label">Risk Level</div>
                            <div class="metric-value" id="risk-level">--</div>
                            <div class="metric-trend" id="risk-trend">
                                <span>Assessment</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="chart-container">
                        <canvas id="prediction-chart" class="chart-canvas"></canvas>
                        
                        <div class="confidence-meter">
                            <div class="confidence-label">AI Confidence</div>
                            <div class="confidence-bar">
                                <div class="confidence-fill" id="confidence-fill"></div>
                            </div>
                        </div>
                        
                        <div class="prediction-timeline">
                            <div class="timeline-item active">
                                <div class="timeline-dot"></div>
                                <div class="timeline-label">Now</div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot"></div>
                                <div class="timeline-label">1h</div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot"></div>
                                <div class="timeline-label">4h</div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot"></div>
                                <div class="timeline-label">1d</div>
                            </div>
                            <div class="timeline-item">
                                <div class="timeline-dot"></div>
                                <div class="timeline-label">Target</div>
                            </div>
                        </div>
                        
                        <div class="loading-animation" id="chart-loading">
                            <div class="loading-spinner"></div>
                        </div>
                    </div>
                </div>
                
                <div class="ai-insights">
                    <div class="insights-header">
                        <div class="ai-icon">AI</div>
                        <div class="insights-title">Market Intelligence</div>
                    </div>
                    <div id="ai-insights-content">
                        <div class="insight-item">Analyzing technical indicators and market sentiment...</div>
                        <div class="insight-item">Processing news sentiment and social signals...</div>
                        <div class="insight-item">Generating probability-weighted predictions...</div>
                    </div>
                </div>
                
                <div class="widget-footer">
                    <div class="last-updated" id="last-updated">Loading...</div>
                    <button class="refresh-btn" id="refresh-predictions">Refresh</button>
                </div>
            </div>
        `;
        
        // Add CSS if not already present
        this.injectCSS();
    }
    
    injectCSS() {
        if (!document.querySelector('#market-widget-styles')) {
            const link = document.createElement('link');
            link.id = 'market-widget-styles';
            link.rel = 'stylesheet';
            link.href = '/static/css/market-widget.css';
            document.head.appendChild(link);
        }
    }
    
    initChart() {
        const canvas = document.getElementById('prediction-chart');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        canvas.width = canvas.offsetWidth * 2;
        canvas.height = canvas.offsetHeight * 2;
        canvas.style.width = canvas.offsetWidth + 'px';
        canvas.style.height = canvas.offsetHeight + 'px';
        ctx.scale(2, 2);
        
        this.chart = {
            canvas,
            ctx,
            data: [],
            predictions: [],
            animation: null
        };
        
        this.drawChart();
    }
    
    bindEvents() {
        // Symbol selection
        this.container.addEventListener('click', (e) => {
            if (e.target.classList.contains('symbol-btn')) {
                this.selectSymbol(e.target.dataset.symbol);
            }
            
            if (e.target.classList.contains('timeframe-btn')) {
                this.selectTimeframe(e.target.dataset.timeframe);
            }
            
            if (e.target.id === 'refresh-predictions') {
                this.refreshPredictions();
            }
        });
        
        // Hover effects for timeline
        const timelineItems = this.container.querySelectorAll('.timeline-item');
        timelineItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                this.highlightTimelinePoint(item);
            });
            
            item.addEventListener('mouseleave', () => {
                this.resetTimeline();
            });
        });
    }
    
    selectSymbol(symbol) {
        if (symbol === this.currentSymbol) return;
        
        // Update UI
        this.container.querySelectorAll('.symbol-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.symbol === symbol);
        });
        
        this.currentSymbol = symbol;
        this.loadPredictions();
    }
    
    selectTimeframe(timeframe) {
        if (timeframe === this.currentTimeframe) return;
        
        // Update UI
        this.container.querySelectorAll('.timeframe-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.timeframe === timeframe);
        });
        
        this.currentTimeframe = timeframe;
        this.loadPredictions();
    }
    
    async loadPredictions() {
        if (this.isLoading) return;
        
        this.setLoading(true);
        
        try {
            const response = await fetch(`${this.options.apiEndpoint}?symbol=${this.currentSymbol}&timeframe=${this.currentTimeframe}`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            this.predictions[this.currentSymbol] = data;
            this.updateUI(data);
            this.animateChart(data);
            
            document.getElementById('prediction-status-text').textContent = 'Active';
            document.getElementById('last-updated').textContent = 
                `Updated ${new Date().toLocaleTimeString()}`;
            
        } catch (error) {
            console.error('Failed to load predictions:', error);
            this.showError(error.message);
        } finally {
            this.setLoading(false);
        }
    }
    
    updateUI(data) {
        // Update metrics
        const priceTarget = document.getElementById('price-target');
        const priceTrend = document.getElementById('price-trend');
        const probability = document.getElementById('prediction-probability');
        const timeTarget = document.getElementById('time-target');
        const riskLevel = document.getElementById('risk-level');
        const riskTrend = document.getElementById('risk-trend');
        
        if (data.prediction) {
            priceTarget.textContent = `$${data.prediction.target_price?.toLocaleString() || '--'}`;
            probability.textContent = `${data.prediction.probability || 0}%`;
            timeTarget.textContent = data.prediction.time_target || '--';
            riskLevel.textContent = data.prediction.risk_level || '--';
            
            // Update trends
            const direction = data.prediction.direction || 'neutral';
            priceTrend.className = `metric-trend trend-${direction}`;
            priceTrend.innerHTML = `<span>${direction === 'up' ? '↗' : direction === 'down' ? '↘' : '→'} ${data.prediction.change_percent || 0}%</span>`;
            
            riskTrend.className = `metric-trend trend-${data.prediction.risk_level?.toLowerCase() || 'neutral'}`;
            riskTrend.innerHTML = `<span>${this.getRiskIcon(data.prediction.risk_level)} ${data.prediction.risk_level || 'Unknown'}</span>`;
        }
        
        // Update confidence meter
        this.updateConfidence(data.confidence || 0);
        
        // Update AI insights
        this.updateInsights(data.insights || []);
    }
    
    updateConfidence(confidence) {
        this.confidence = confidence;
        const fill = document.getElementById('confidence-fill');
        if (fill) {
            fill.style.width = `${confidence}%`;
        }
    }
    
    updateInsights(insights) {
        const container = document.getElementById('ai-insights-content');
        if (!container || !insights.length) return;
        
        container.innerHTML = insights.map(insight => 
            `<div class="insight-item fade-in">${insight}</div>`
        ).join('');
    }
    
    getRiskIcon(riskLevel) {
        const icons = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴',
            'critical': '⛔'
        };
        return icons[riskLevel?.toLowerCase()] || '⚪';
    }
    
    drawChart() {
        if (!this.chart) return;
        
        const { ctx, canvas } = this.chart;
        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw background grid
        this.drawGrid(ctx, width, height);
        
        // Draw prediction line
        if (this.chart.predictions.length > 0) {
            this.drawPredictionLine(ctx, width, height);
        }
        
        // Draw current data
        if (this.chart.data.length > 0) {
            this.drawDataLine(ctx, width, height);
        }
    }
    
    drawGrid(ctx, width, height) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        
        // Horizontal lines
        for (let i = 0; i <= 4; i++) {
            const y = (height * i) / 4;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        // Vertical lines
        for (let i = 0; i <= 6; i++) {
            const x = (width * i) / 6;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
    }
    
    drawDataLine(ctx, width, height) {
        if (this.chart.data.length < 2) return;
        
        ctx.strokeStyle = '#64ffda';
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        this.chart.data.forEach((point, index) => {
            const x = (width * index) / (this.chart.data.length - 1);
            const y = height - (height * point.normalized);
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
    }
    
    drawPredictionLine(ctx, width, height) {
        if (this.chart.predictions.length < 2) return;
        
        ctx.strokeStyle = '#ffd93d';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        
        this.chart.predictions.forEach((point, index) => {
            const x = width * 0.6 + (width * 0.4 * index) / (this.chart.predictions.length - 1);
            const y = height - (height * point.normalized);
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    animateChart(data) {
        // Simulate chart data for animation
        const mockData = this.generateMockChartData();
        const mockPredictions = this.generateMockPredictions();
        
        this.chart.data = mockData;
        this.chart.predictions = mockPredictions;
        
        // Animate drawing
        let progress = 0;
        const animate = () => {
            progress += 0.02;
            if (progress <= 1) {
                this.drawAnimatedChart(progress);
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
    
    drawAnimatedChart(progress) {
        if (!this.chart) return;
        
        const { ctx, canvas } = this.chart;
        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        
        ctx.clearRect(0, 0, width, height);
        this.drawGrid(ctx, width, height);
        
        // Draw data up to progress
        if (this.chart.data.length > 0) {
            const visiblePoints = Math.floor(this.chart.data.length * progress);
            const visibleData = this.chart.data.slice(0, visiblePoints);
            
            if (visibleData.length > 1) {
                ctx.strokeStyle = '#64ffda';
                ctx.lineWidth = 2;
                ctx.beginPath();
                
                visibleData.forEach((point, index) => {
                    const x = (width * 0.6 * index) / (this.chart.data.length - 1);
                    const y = height - (height * point.normalized);
                    
                    if (index === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                
                ctx.stroke();
            }
        }
        
        // Draw predictions if data animation is complete
        if (progress > 0.6 && this.chart.predictions.length > 0) {
            const predictionProgress = (progress - 0.6) / 0.4;
            const visiblePredictions = Math.floor(this.chart.predictions.length * predictionProgress);
            const visiblePredData = this.chart.predictions.slice(0, visiblePredictions);
            
            if (visiblePredData.length > 1) {
                ctx.strokeStyle = '#ffd93d';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                
                visiblePredData.forEach((point, index) => {
                    const x = width * 0.6 + (width * 0.4 * index) / (this.chart.predictions.length - 1);
                    const y = height - (height * point.normalized);
                    
                    if (index === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                
                ctx.stroke();
                ctx.setLineDash([]);
            }
        }
    }
    
    generateMockChartData() {
        const data = [];
        let price = 50000 + Math.random() * 20000; // Base price
        
        for (let i = 0; i < 20; i++) {
            price += (Math.random() - 0.5) * 2000;
            data.push({
                price,
                normalized: (price - 40000) / 40000 // Normalize for drawing
            });
        }
        
        return data;
    }
    
    generateMockPredictions() {
        const predictions = [];
        const lastPrice = this.chart.data[this.chart.data.length - 1]?.price || 60000;
        let price = lastPrice;
        
        for (let i = 0; i < 10; i++) {
            price += (Math.random() - 0.4) * 1000; // Slight upward bias
            predictions.push({
                price,
                normalized: (price - 40000) / 40000
            });
        }
        
        return predictions;
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        const loadingEl = document.getElementById('chart-loading');
        if (loadingEl) {
            loadingEl.style.display = loading ? 'block' : 'none';
        }
    }
    
    showError(message) {
        const statusEl = document.getElementById('prediction-status-text');
        if (statusEl) {
            statusEl.textContent = `Error: ${message}`;
            statusEl.style.color = '#ff6b6b';
        }
    }
    
    highlightTimelinePoint(item) {
        // Add hover effect logic
        item.style.opacity = '1';
        item.style.transform = 'scale(1.1)';
    }
    
    resetTimeline() {
        const items = this.container.querySelectorAll('.timeline-item');
        items.forEach(item => {
            item.style.opacity = '';
            item.style.transform = '';
        });
    }
    
    refreshPredictions() {
        this.loadPredictions();
    }
    
    startUpdates() {
        setInterval(() => {
            this.loadPredictions();
        }, this.options.updateInterval);
    }
    
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        if (this.chart && this.chart.animation) {
            cancelAnimationFrame(this.chart.animation);
        }
        
        this.container.innerHTML = '';
    }
}

// Auto-initialize if container exists
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('market-prediction-widget');
    if (container) {
        window.marketPredictionWidget = new MarketPredictionWidget('market-prediction-widget');
    }
});