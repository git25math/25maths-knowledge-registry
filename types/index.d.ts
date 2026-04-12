/**
 * 25maths Knowledge Registry — TypeScript type definitions
 *
 * Auto-generated from dist/ artifact structures.
 * Import: import type { MetaNode, Route, ... } from 'knowledge-registry/types';
 */

// ══════════════════════════════════════════
// Core types
// ══════════════════════════════════════════

export type Domain = 'number' | 'algebra' | 'geometry' | 'statistics' | 'probability';
export type PrimaryBoard = 'cie' | 'edx' | 'both';
export type Tier = 'core' | 'extended' | 'both' | 'higher' | 'foundation';
export type Weight = 'highest' | 'high' | 'medium' | 'low' | 'rare';
export type PrerequisiteType = 'hard' | 'soft';

// ══════════════════════════════════════════
// dist/meta-nodes.json
// ══════════════════════════════════════════

export interface MetaNode {
  kn_id: string;
  title_en: string;
  title_zh: string;
  domain: Domain;
  subdomain: string;
  primaryBoard: PrimaryBoard;

  examBoards: {
    cie_0580?: CieExamBoard;
    edexcel_4ma1?: EdexcelExamBoard;
    hhk?: HhkExamBoard;
  };

  prerequisites: Prerequisite[];
  leadsTo: string[];
  variantOf?: string | null;

  content: {
    variants: {
      cie: string[];
      edexcel: string[];
      generic: string[];
    };
    missions: number[];
    glGeneratorId: string | null;
    examRefs: {
      cie: number;
      edexcel: number;
    };
  };

  learning: {
    estimatedMinutes: {
      concept: number;
      practice: number;
    };
    difficultyRange: [number, number];
    noFigure: boolean;
    isFoundational: boolean;
  };

  routes: string[];
  version: number;
  createdAt: string;
}

export interface CieExamBoard {
  section: string;
  tier: Tier;
  weight: Weight;
  paperCodes?: string[];
}

export interface EdexcelExamBoard {
  section: string;
  tier: Tier;
  weight: Weight;
}

export interface HhkExamBoard {
  units: string[];
  year: number;
}

export interface Prerequisite {
  kn_id: string;
  type: PrerequisiteType;
}

// ══════════════════════════════════════════
// dist/routes-compiled.json
// ══════════════════════════════════════════

export interface RoutesCompiled {
  [routeId: string]: Route;
}

export interface Route {
  id: string;
  title_en: string;
  title_zh: string;
  board: string;
  tier: string;
  description: string;
  estimatedHours: number;
  boardFilter: PrimaryBoard[];
  nodes: (RouteNode | MilestoneNode)[];
  version: number;
  createdAt: string;
}

export interface RouteNode {
  kn_id: string;
  order: number;
  isRequired: boolean;
  unlockCondition: {
    type: 'prerequisite_mastered';
    threshold: number;
  };
  estimatedMinutes: number;
  milestone: false;
}

export interface MilestoneNode {
  kn_id: string;
  type: 'milestone';
  order: number;
  title_en: string;
  title_zh: string;
  covers: string[];
  isRequired: false;
  milestone: true;
}

// ══════════════════════════════════════════
// dist/nodes-by-board.json
// ══════════════════════════════════════════

export interface NodesByBoard {
  cie_view: BoardNodeEntry[];
  edx_view: BoardNodeEntry[];
  cie_only: BoardNodeEntry[];
  edx_only: BoardNodeEntry[];
  both: BoardNodeEntry[];
}

export interface BoardNodeEntry {
  kn_id: string;
  title_en: string;
  title_zh: string;
  domain: Domain;
  subdomain: string;
  difficultyRange: [number, number];
}

// ══════════════════════════════════════════
// dist/question-id-map.json
// ══════════════════════════════════════════

export interface QuestionIdMap {
  [knId: string]: {
    cie?: string;   // e.g. "cie.1.4"
    edx?: string;   // e.g. "edx.ch1-u7"
  };
}

// ══════════════════════════════════════════
// dist/board-stats.json
// ══════════════════════════════════════════

export interface BoardStats {
  cie: BoardStatEntry;
  edx: BoardStatEntry;
  both: BoardStatEntry;
}

export interface BoardStatEntry {
  total: number;
  domains: Partial<Record<Domain, number>>;
}

// ══════════════════════════════════════════
// dist/build-manifest.json
// ══════════════════════════════════════════

export interface BuildManifest {
  generatedBy: string;
  sourceHashes: Record<string, string>;
  distFiles: Record<string, string>;
}

// ══════════════════════════════════════════
// registry/kp-kn-map.json
// ══════════════════════════════════════════

export type KpKnMap = Record<string, string>;

// ══════════════════════════════════════════
// graph/dag-edges.json
// ══════════════════════════════════════════

export interface DagEdge {
  from: string;
  to: string;
  type: PrerequisiteType;
}
