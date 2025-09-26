#!/usr/bin/env python3
"""
Example usage for JavaScript/TypeScript projects.

This example shows specific tasks that work well with JS/TS codebases.
"""

import sys
from pathlib import Path

# Add parent directory to path to import our orchestrator modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator_standalone import StandaloneOrchestrator
from src.agents.env_interaction.command_executor import LocalExecutor


def example_javascript_tasks():
    """Example tasks specifically useful for JavaScript/TypeScript projects."""
    
    javascript_tasks = [
        # Testing tasks
        "Add Jest unit tests for all React components with proper mocking and snapshot testing",
        "Create end-to-end tests using Playwright or Cypress for critical user flows",
        "Add React Testing Library tests with proper accessibility and user interaction testing",
        "Implement integration tests for API endpoints using supertest and proper test database setup",
        
        # TypeScript tasks
        "Convert JavaScript codebase to TypeScript with proper type definitions and strict mode",
        "Add comprehensive TypeScript interfaces and types for all API responses and data models",
        "Configure TypeScript with strict settings and fix all type errors",
        
        # React-specific tasks
        "Add React components with proper props validation using PropTypes or TypeScript",
        "Implement React hooks for state management replacing class components",
        "Add React Context API for global state management with proper typing",
        "Create reusable UI components with Storybook documentation and examples",
        "Implement React error boundaries for better error handling and user experience",
        
        # Vue.js-specific tasks
        "Add Vue 3 Composition API components with proper reactivity and TypeScript support",
        "Implement Vuex store for state management with proper modules and mutations",
        "Add Vue Router with proper navigation guards and lazy loading",
        
        # Node.js/Express tasks
        "Add Express middleware for authentication, logging, and error handling",
        "Implement proper Express route validation using Joi or similar schema validation",
        "Add Express API rate limiting and security headers middleware",
        "Create Express REST API with proper HTTP status codes and error responses",
        
        # Build and tooling tasks
        "Configure Webpack with proper optimization, code splitting, and production builds",
        "Add ESLint and Prettier configuration with consistent code formatting rules",
        "Implement Vite build system with proper development and production configurations",
        "Add Rollup configuration for library bundling with proper tree shaking",
        
        # Performance tasks
        "Implement lazy loading and code splitting for improved bundle size and performance",
        "Add service worker for caching and offline functionality",
        "Optimize images and assets with proper compression and modern formats",
        "Add performance monitoring with Web Vitals and proper metrics collection",
        
        # State management tasks
        "Implement Redux with Redux Toolkit for predictable state management",
        "Add Zustand for lightweight state management with proper TypeScript support",
        "Create MobX store with proper observable state and computed values",
        
        # UI and styling tasks
        "Add Tailwind CSS with proper configuration and custom design tokens",
        "Implement CSS-in-JS styling using styled-components or emotion",
        "Add responsive design with proper breakpoints and mobile-first approach",
        "Create design system components with consistent styling and theming",
        
        # API and data fetching tasks
        "Add React Query or SWR for server state management and caching",
        "Implement GraphQL client with Apollo or similar for efficient data fetching",
        "Add proper error handling and loading states for all API calls",
        "Create API mock service using MSW for development and testing",
        
        # Security tasks
        "Add Content Security Policy headers and XSS protection",
        "Implement proper input sanitization and validation on client side",
        "Add CSRF protection for forms and API requests",
        
        # Accessibility tasks
        "Add proper ARIA labels and semantic HTML for screen reader compatibility",
        "Implement keyboard navigation support for all interactive elements",
        "Add color contrast checking and alternative text for images",
        
        # PWA tasks
        "Convert web app to Progressive Web App with service worker and manifest",
        "Add offline functionality with proper cache strategies",
        "Implement push notifications with proper user consent handling",
    ]
    
    return javascript_tasks


def run_javascript_task_example(repo_path: str = "."):
    """Run an example JavaScript task."""
    
    # Create executor for the repository
    executor = LocalExecutor(working_directory=repo_path)
    
    # Create orchestrator
    orchestrator = StandaloneOrchestrator(
        model="anthropic/claude-sonnet-4-20250514",
        temperature=0.1
    )
    
    # Setup orchestrator
    orchestrator.setup(executor)
    
    # Example task: Add comprehensive React testing
    task = "Add React Testing Library tests for all components with proper user interaction testing and accessibility checks"
    
    print(f"🚀 Running JavaScript-specific task on {repo_path}")
    print(f"📋 Task: {task}")
    print("-" * 80)
    
    # Execute the task
    result = orchestrator.run(task, max_turns=35)
    
    print(f"\n📊 Results:")
    print(f"Completed: {result['completed']}")
    print(f"Message: {result['finish_message']}")
    print(f"Turns: {result['turns_executed']}")
    
    return result


def main():
    """Main example runner."""
    print("🚀 JavaScript/TypeScript Project Examples for Orchestrator")
    print("=" * 70)
    
    tasks = example_javascript_tasks()
    
    print(f"\n📋 {len(tasks)} Example JavaScript/TypeScript Tasks:")
    for i, task in enumerate(tasks[:12], 1):  # Show first 12
        print(f"{i:2}. {task}")
    
    if len(tasks) > 12:
        print(f"    ... and {len(tasks) - 12} more!")
    
    print(f"\n🚀 Example Usage:")
    print(f"python orchestrator_cli.py \"{tasks[0]}\"")
    
    print(f"\n💡 Tips for JavaScript/TypeScript Projects:")
    print("• Specify frameworks: 'Add React components' vs 'Add components'")
    print("• Mention testing libraries: 'Add Jest tests' vs 'Add unit tests'")
    print("• Include build tools: 'Configure Webpack' vs 'Set up bundling'")
    print("• Specify TypeScript when relevant: 'Add TypeScript interfaces'")
    print("• Mention performance: 'Add lazy loading for better performance'")
    
    print(f"\n🔧 Common JavaScript Project Patterns:")
    print("• React + TypeScript + Jest + React Testing Library")
    print("• Vue 3 + TypeScript + Vitest + Vue Test Utils")
    print("• Node.js + Express + TypeScript + Jest + Supertest")
    print("• Next.js + TypeScript + Playwright + Tailwind CSS")
    
    # Uncomment to run an actual example (requires API key)
    # run_javascript_task_example(".")


if __name__ == "__main__":
    main()