require('dotenv').config();

const express = require('express');
const cors = require('cors');
const { sequelize } = require('./models');
const routes = require('./routes/index');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api', routes);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: 'Something went wrong!',
        message: err.message 
    });
});

const PORT = process.env.PORT || 3000;

async function startServer() {
    try {
        // Database connection
        await sequelize.authenticate();
        console.log('Database connected successfully');

        // Start server
        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });
    } catch (error) {
        console.error('Unable to start server:', error);
    }
}

startServer();

module.exports = app;