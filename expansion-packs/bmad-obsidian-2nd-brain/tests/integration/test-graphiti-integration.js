#!/usr/bin/env node

/**
 * Graphiti MCP Integration Test (REFERENCE IMPLEMENTATION)
 *
 * ⚠️ IMPORTANT: This test file is a REFERENCE IMPLEMENTATION only.
 *
 * The actual Graphiti MCP server uses STDIO transport (via MCP protocol), not HTTP REST.
 * This test assumes a hypothetical HTTP wrapper around Graphiti MCP operations.
 *
 * ACTUAL GRAPHITI MCP INTEGRATION:
 * - Uses stdio transport configured in claude_desktop_config.json
 * - Communicates via Model Context Protocol (MCP) standard
 * - Tools: add_episode, get_episodes, add_entity, add_relation
 * - Cannot be tested via HTTP endpoints without custom wrapper
 *
 * TO USE THIS TEST FILE:
 * Option 1: Create an HTTP wrapper around Graphiti MCP stdio server
 *   - Implement HTTP endpoints that proxy to Graphiti MCP tools
 *   - Expose endpoints at http://localhost:8000/mcp/*
 *   - Map HTTP requests to MCP tool calls
 *
 * Option 2: Test via actual agent usage (RECOMMENDED)
 *   - Use inbox-triage-agent to create capture events
 *   - Use semantic-linker-agent to create relationships
 *   - Use query-interpreter-agent to retrieve episodes
 *   - Verify in Neo4j Browser: http://localhost:7474
 *
 * Option 3: Direct Neo4j testing (ALTERNATIVE)
 *   - Use test-neo4j-connection.js to verify database
 *   - Manually create nodes via Neo4j Browser
 *   - Test Cypher queries from examples/neo4j/temporal-queries.cypher
 *
 * This file demonstrates the EXPECTED data structures and operations,
 * but should not be run as-is without an HTTP wrapper implementation.
 *
 * Comprehensive test of Graphiti MCP operations for Phase 1:
 * - add_episode (create CaptureEvent nodes)
 * - get_episodes (retrieve by time range)
 * - add_entity (create Note nodes)
 * - add_relation (create LINKED_TO relationships)
 *
 * Prerequisites (if using HTTP wrapper):
 * 1. Neo4j running (docker compose -f docker-compose.neo4j.yml up -d)
 * 2. Graphiti MCP HTTP wrapper running on port 8000
 * 3. Environment variables configured (.env file)
 *
 * Run: node expansion-packs/bmad-obsidian-2nd-brain/tests/integration/test-graphiti-integration.js
 */

const http = require('http');

// =============================================================================
// Configuration
// =============================================================================

const CONFIG = {
  host: process.env.GRAPHITI_HOST || 'localhost',
  port: parseInt(process.env.GRAPHITI_PORT) || 8000,
  timeout: 10000, // 10 seconds per operation
};

// Test data
const TEST_PREFIX = `test-${Date.now()}`;
const SAMPLE_NOTES = [
  {
    id: `${TEST_PREFIX}-note-1`,
    path: 'atomic/spaced-repetition-superior.md',
    title: 'Spaced Repetition Superior to Massed Practice',
    tags: ['learning', 'memory', 'cognitive-science'],
    content_hash: 'abc123',
    word_count: 487,
  },
  {
    id: `${TEST_PREFIX}-note-2`,
    path: 'atomic/forgetting-curve.md',
    title: 'Ebbinghaus Forgetting Curve',
    tags: ['memory', 'cognitive-psychology', 'ebbinghaus'],
    content_hash: 'def456',
    word_count: 312,
  },
  {
    id: `${TEST_PREFIX}-note-3`,
    path: 'atomic/testing-effect.md',
    title: 'Testing Effect Enhances Retention',
    tags: ['learning', 'memory', 'retrieval'],
    content_hash: 'ghi789',
    word_count: 254,
  },
];

const SAMPLE_EPISODES = [
  {
    id: `${TEST_PREFIX}-episode-1`,
    timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 7 days ago
    capture_method: 'inbox',
    source_url: 'https://example.com/article-1',
    note_id: `${TEST_PREFIX}-note-1`,
  },
  {
    id: `${TEST_PREFIX}-episode-2`,
    timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
    capture_method: 'web-clipper',
    source_url: 'https://example.com/article-2',
    note_id: `${TEST_PREFIX}-note-2`,
  },
  {
    id: `${TEST_PREFIX}-episode-3`,
    timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
    capture_method: 'manual',
    note_id: `${TEST_PREFIX}-note-3`,
  },
];

const SAMPLE_RELATIONS = [
  {
    source_id: `${TEST_PREFIX}-note-2`,
    target_id: `${TEST_PREFIX}-note-1`,
    relation_type: 'supports',
    confidence: 0.87,
    strength: 0.82,
    context_forward: 'The forgetting curve provides empirical evidence for spaced repetition',
    context_backward: 'Spaced repetition is supported by the forgetting curve phenomenon',
  },
  {
    source_id: `${TEST_PREFIX}-note-3`,
    target_id: `${TEST_PREFIX}-note-1`,
    relation_type: 'supports',
    confidence: 0.85,
    strength: 0.78,
    context_forward: 'The testing effect demonstrates the superiority of active retrieval',
    context_backward: 'Spaced repetition benefits from the testing effect',
  },
];

// =============================================================================
// Utility Functions
// =============================================================================

function makeRequest(options, data = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let responseBody = '';

      res.on('data', (chunk) => {
        responseBody += chunk;
      });

      res.on('end', () => {
        try {
          const parsedData = responseBody ? JSON.parse(responseBody) : {};
          resolve({
            status: res.statusCode,
            data: parsedData,
            headers: res.headers,
          });
        } catch (error) {
          resolve({
            status: res.statusCode,
            data: responseBody,
            headers: res.headers,
          });
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

function printSection(title) {
  console.log('\n' + '='.repeat(80));
  console.log(title);
  console.log('='.repeat(80));
}

function printTest(name, result) {
  const status = result.success ? '✓' : '✗';
  const color = result.success ? '\x1b[32m' : '\x1b[31m';
  const reset = '\x1b[0m';

  console.log(`${color}${status}${reset} ${name}`);

  if (result.data) {
    console.log(`  Data: ${JSON.stringify(result.data, null, 2).substring(0, 200)}...`);
  }

  if (result.error) {
    console.log(`  Error: ${result.error}`);
  }

  if (result.duration) {
    console.log(`  Duration: ${result.duration}ms`);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// =============================================================================
// Test Functions
// =============================================================================

async function testAddEpisode(episodeData) {
  const startTime = Date.now();

  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/add_episode',
      method: 'POST',
      timeout: CONFIG.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const requestData = {
      episode_id: episodeData.id,
      timestamp: episodeData.timestamp,
      metadata: {
        capture_method: episodeData.capture_method,
        source_url: episodeData.source_url || null,
        note_id: episodeData.note_id,
      },
    };

    const response = await makeRequest(options, requestData);
    const duration = Date.now() - startTime;

    if (response.status === 200 || response.status === 201) {
      return {
        success: true,
        data: response.data,
        duration,
      };
    } else {
      return {
        success: false,
        error: `HTTP ${response.status}: ${JSON.stringify(response.data)}`,
        duration,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      duration: Date.now() - startTime,
    };
  }
}

async function testGetEpisodes(startDate, endDate) {
  const startTime = Date.now();

  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/get_episodes',
      method: 'POST',
      timeout: CONFIG.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const requestData = {
      start_date: startDate,
      end_date: endDate,
    };

    const response = await makeRequest(options, requestData);
    const duration = Date.now() - startTime;

    if (response.status === 200) {
      return {
        success: true,
        data: response.data,
        duration,
      };
    } else {
      return {
        success: false,
        error: `HTTP ${response.status}: ${JSON.stringify(response.data)}`,
        duration,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      duration: Date.now() - startTime,
    };
  }
}

async function testAddEntity(noteData) {
  const startTime = Date.now();

  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/add_entity',
      method: 'POST',
      timeout: CONFIG.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const requestData = {
      entity_id: noteData.id,
      entity_type: 'Note',
      properties: {
        path: noteData.path,
        title: noteData.title,
        tags: noteData.tags,
        content_hash: noteData.content_hash,
        word_count: noteData.word_count,
        created_at: new Date().toISOString(),
      },
    };

    const response = await makeRequest(options, requestData);
    const duration = Date.now() - startTime;

    if (response.status === 200 || response.status === 201) {
      return {
        success: true,
        data: response.data,
        duration,
      };
    } else {
      return {
        success: false,
        error: `HTTP ${response.status}: ${JSON.stringify(response.data)}`,
        duration,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      duration: Date.now() - startTime,
    };
  }
}

async function testAddRelation(relationData) {
  const startTime = Date.now();

  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/add_relation',
      method: 'POST',
      timeout: CONFIG.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const requestData = {
      source_entity_id: relationData.source_id,
      target_entity_id: relationData.target_id,
      relation_type: 'CONCEPTUALLY_RELATED',
      properties: {
        link_type: relationData.relation_type,
        confidence: relationData.confidence,
        strength: relationData.strength,
        semantic_similarity: relationData.strength * 0.9,
        created_at: new Date().toISOString(),
        created_by: 'semantic-linker-agent',
        context_forward: relationData.context_forward,
        context_backward: relationData.context_backward,
      },
    };

    const response = await makeRequest(options, requestData);
    const duration = Date.now() - startTime;

    if (response.status === 200 || response.status === 201) {
      return {
        success: true,
        data: response.data,
        duration,
      };
    } else {
      return {
        success: false,
        error: `HTTP ${response.status}: ${JSON.stringify(response.data)}`,
        duration,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      duration: Date.now() - startTime,
    };
  }
}

async function testCleanup() {
  const startTime = Date.now();

  try {
    const options = {
      hostname: CONFIG.host,
      port: CONFIG.port,
      path: '/mcp/delete_test_data',
      method: 'POST',
      timeout: CONFIG.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const requestData = {
      prefix: TEST_PREFIX,
    };

    const response = await makeRequest(options, requestData);
    const duration = Date.now() - startTime;

    if (response.status === 200) {
      return {
        success: true,
        data: response.data,
        duration,
      };
    } else {
      // Cleanup endpoint might not exist - that's okay
      return {
        success: true,
        error: 'Cleanup endpoint not available (manual cleanup required)',
        duration,
      };
    }
  } catch (error) {
    return {
      success: true, // Don't fail test if cleanup fails
      error: `Cleanup failed: ${error.message} (manual cleanup required)`,
      duration: Date.now() - startTime,
    };
  }
}

// =============================================================================
// Main Test Suite
// =============================================================================

async function runIntegrationTests() {
  console.log('Graphiti MCP Integration Test Suite');
  console.log('====================================\n');
  console.log(`Test prefix: ${TEST_PREFIX}`);
  console.log(`Graphiti endpoint: http://${CONFIG.host}:${CONFIG.port}`);
  console.log(`Timeout: ${CONFIG.timeout}ms\n`);

  let allTestsPassed = true;
  const results = {
    add_episode: [],
    add_entity: [],
    add_relation: [],
    get_episodes: null,
    cleanup: null,
  };

  // -------------------------------------------------------------------------
  // Phase 1: Create Episodes (CaptureEvents)
  // -------------------------------------------------------------------------

  printSection('Phase 1: Testing add_episode (Create CaptureEvents)');

  for (const episode of SAMPLE_EPISODES) {
    const result = await testAddEpisode(episode);
    results.add_episode.push(result);
    printTest(`Create episode: ${episode.id}`, result);

    if (!result.success) {
      allTestsPassed = false;
    }

    await sleep(100); // Small delay between operations
  }

  // -------------------------------------------------------------------------
  // Phase 2: Create Entities (Notes)
  // -------------------------------------------------------------------------

  printSection('Phase 2: Testing add_entity (Create Note Entities)');

  for (const note of SAMPLE_NOTES) {
    const result = await testAddEntity(note);
    results.add_entity.push(result);
    printTest(`Create note entity: ${note.title}`, result);

    if (!result.success) {
      allTestsPassed = false;
    }

    await sleep(100);
  }

  // -------------------------------------------------------------------------
  // Phase 3: Create Relations (Semantic Links)
  // -------------------------------------------------------------------------

  printSection('Phase 3: Testing add_relation (Create Semantic Links)');

  for (const relation of SAMPLE_RELATIONS) {
    const result = await testAddRelation(relation);
    results.add_relation.push(result);
    const sourceNote = SAMPLE_NOTES.find(n => n.id === relation.source_id);
    const targetNote = SAMPLE_NOTES.find(n => n.id === relation.target_id);
    printTest(
      `Create relation: ${sourceNote?.title} → ${targetNote?.title} (${relation.relation_type})`,
      result
    );

    if (!result.success) {
      allTestsPassed = false;
    }

    await sleep(100);
  }

  // -------------------------------------------------------------------------
  // Phase 4: Retrieve Episodes (Temporal Queries)
  // -------------------------------------------------------------------------

  printSection('Phase 4: Testing get_episodes (Temporal Queries)');

  const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(); // 30 days ago
  const endDate = new Date().toISOString();

  const getEpisodesResult = await testGetEpisodes(startDate, endDate);
  results.get_episodes = getEpisodesResult;
  printTest(`Retrieve episodes (last 30 days)`, getEpisodesResult);

  if (!getEpisodesResult.success) {
    allTestsPassed = false;
  }

  // Verify we got back our test episodes
  if (getEpisodesResult.success && getEpisodesResult.data) {
    const retrievedCount = Array.isArray(getEpisodesResult.data.episodes)
      ? getEpisodesResult.data.episodes.length
      : 0;

    console.log(`  Retrieved ${retrievedCount} episodes`);

    if (retrievedCount >= SAMPLE_EPISODES.length) {
      console.log(`  ✓ All test episodes retrieved`);
    } else {
      console.log(`  ⚠️ Expected at least ${SAMPLE_EPISODES.length} episodes`);
    }
  }

  // -------------------------------------------------------------------------
  // Phase 5: Performance Summary
  // -------------------------------------------------------------------------

  printSection('Phase 5: Performance Summary');

  const avgEpisodeDuration =
    results.add_episode.reduce((sum, r) => sum + (r.duration || 0), 0) /
    results.add_episode.length;

  const avgEntityDuration =
    results.add_entity.reduce((sum, r) => sum + (r.duration || 0), 0) /
    results.add_entity.length;

  const avgRelationDuration =
    results.add_relation.reduce((sum, r) => sum + (r.duration || 0), 0) /
    results.add_relation.length;

  console.log(`Average add_episode duration: ${avgEpisodeDuration.toFixed(0)}ms`);
  console.log(`Average add_entity duration: ${avgEntityDuration.toFixed(0)}ms`);
  console.log(`Average add_relation duration: ${avgRelationDuration.toFixed(0)}ms`);
  console.log(`get_episodes duration: ${results.get_episodes?.duration || 0}ms`);

  // Performance thresholds (all operations should be < 1000ms)
  const performanceThreshold = 1000;
  const performanceWarnings = [];

  if (avgEpisodeDuration > performanceThreshold) {
    performanceWarnings.push(`add_episode too slow (${avgEpisodeDuration.toFixed(0)}ms > ${performanceThreshold}ms)`);
  }

  if (avgEntityDuration > performanceThreshold) {
    performanceWarnings.push(`add_entity too slow (${avgEntityDuration.toFixed(0)}ms > ${performanceThreshold}ms)`);
  }

  if (avgRelationDuration > performanceThreshold) {
    performanceWarnings.push(`add_relation too slow (${avgRelationDuration.toFixed(0)}ms > ${performanceThreshold}ms)`);
  }

  if (results.get_episodes?.duration > performanceThreshold) {
    performanceWarnings.push(`get_episodes too slow (${results.get_episodes.duration}ms > ${performanceThreshold}ms)`);
  }

  if (performanceWarnings.length > 0) {
    console.log('\n⚠️  Performance Warnings:');
    performanceWarnings.forEach(w => console.log(`  - ${w}`));
  } else {
    console.log('\n✓ All operations within performance budget (<1000ms)');
  }

  // -------------------------------------------------------------------------
  // Phase 6: Cleanup
  // -------------------------------------------------------------------------

  printSection('Phase 6: Cleanup Test Data');

  const cleanupResult = await testCleanup();
  results.cleanup = cleanupResult;
  printTest('Clean up test data', cleanupResult);

  if (cleanupResult.error) {
    console.log('\n⚠️  Manual cleanup required:');
    console.log(`  Run in Neo4j Browser:`);
    console.log(`  MATCH (n) WHERE n.note_id STARTS WITH "${TEST_PREFIX}" OR n.episode_id STARTS WITH "${TEST_PREFIX}" DETACH DELETE n;`);
  }

  // -------------------------------------------------------------------------
  // Final Summary
  // -------------------------------------------------------------------------

  printSection('Test Summary');

  const totalTests =
    results.add_episode.length +
    results.add_entity.length +
    results.add_relation.length +
    1; // get_episodes

  const passedTests =
    results.add_episode.filter(r => r.success).length +
    results.add_entity.filter(r => r.success).length +
    results.add_relation.filter(r => r.success).length +
    (results.get_episodes?.success ? 1 : 0);

  console.log(`Total tests: ${totalTests}`);
  console.log(`Passed: ${passedTests}`);
  console.log(`Failed: ${totalTests - passedTests}`);
  console.log(`Success rate: ${((passedTests / totalTests) * 100).toFixed(1)}%`);

  if (allTestsPassed && passedTests === totalTests) {
    console.log('\n✓ All integration tests passed!');
    console.log('\nNext steps:');
    console.log('1. Verify data in Neo4j Browser: http://localhost:7474');
    console.log('2. Run temporal queries from examples/neo4j/temporal-queries.cypher');
    console.log('3. Test agents with Neo4j integration enabled');
    return 0;
  } else {
    console.log('\n✗ Some tests failed. Please review errors above.');
    console.log('\nTroubleshooting:');
    console.log('1. Verify Neo4j is running: docker compose -f docker-compose.neo4j.yml ps');
    console.log('2. Verify Graphiti MCP server is running');
    console.log('3. Check environment variables in .env file');
    console.log('4. Review Graphiti MCP logs for errors');
    return 1;
  }
}

// =============================================================================
// Run Tests
// =============================================================================

runIntegrationTests()
  .then((exitCode) => {
    process.exit(exitCode);
  })
  .catch((error) => {
    console.error('\n❌ Fatal error:', error);
    process.exit(1);
  });
