const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const db = require('../models/database');

// Simple auth middleware
const authenticate = async (req, res, next) => {
  const { password } = req.body;
  
  if (!password || password !== process.env.ADMIN_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  next();
};

// Create new poll
router.post('/polls', authenticate, async (req, res) => {
  try {
    const { title, description, questions } = req.body;

    // Insert poll
    const pollResult = await db.run(
      'INSERT INTO polls (title, description) VALUES (?, ?)',
      [title, description]
    );
    
    const pollId = pollResult.id;

    // Insert questions and options
    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];
      const questionResult = await db.run(
        'INSERT INTO questions (poll_id, question_text, question_type, order_index) VALUES (?, ?, ?, ?)',
        [pollId, question.text, question.type || 'single', i]
      );
      
      const questionId = questionResult.id;

      // Insert options for this question
      for (let j = 0; j < question.options.length; j++) {
        await db.run(
          'INSERT INTO options (question_id, option_text, order_index) VALUES (?, ?, ?)',
          [questionId, question.options[j], j]
        );
      }
    }

    res.json({ success: true, pollId });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update poll status
router.put('/polls/:id/status', authenticate, async (req, res) => {
  try {
    const { active } = req.body;
    const pollId = req.params.id;

    await db.run(
      'UPDATE polls SET active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [active ? 1 : 0, pollId]
    );

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Close poll voting
router.put('/polls/:id/close', authenticate, async (req, res) => {
  try {
    const pollId = req.params.id;

    await db.run(
      'UPDATE polls SET closed = 1, closed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [pollId]
    );

    // Emit poll closed event via WebSocket
    const io = req.app.get('io');
    if (io) {
      io.to(`poll-${pollId}`).emit('pollClosed', { pollId });
    }

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete poll
router.delete('/polls/:id', authenticate, async (req, res) => {
  try {
    const pollId = req.params.id;

    await db.run('DELETE FROM polls WHERE id = ?', [pollId]);

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all polls (including inactive)
router.post('/polls/list', authenticate, async (req, res) => {
  try {
    const polls = await db.all('SELECT * FROM polls ORDER BY created_at DESC');
    
    for (let poll of polls) {
      const voteCount = await db.get(`
        SELECT COUNT(DISTINCT v.session_id) as participant_count
        FROM votes v
        JOIN options o ON v.option_id = o.id
        JOIN questions q ON o.question_id = q.id
        WHERE q.poll_id = ?
      `, [poll.id]);
      
      poll.participant_count = voteCount.participant_count;
    }

    res.json(polls);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;