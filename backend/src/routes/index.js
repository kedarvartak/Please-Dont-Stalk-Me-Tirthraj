const express = require('express');
const router = express.Router();
const { sequelize } = require('../models');
const chatController = require('../controllers/chatController');

router.get('/test-db', async (req, res) => {
    try {
        await sequelize.authenticate();
        res.json({ message: 'Database connection successful' });
    } catch (error) {
        console.error('Database connection error:', error);
        res.status(500).json({ error: 'Database connection failed' });
    }
});

// Chat routes
router.post('/chat', chatController.processQuery);

module.exports = router; 