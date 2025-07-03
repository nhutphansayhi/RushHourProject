#!/usr/bin/env python3
"""
Demo script showing the multi-algorithm functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.utils import import_map
from utils.state import State
from solver.bfs_solver import bfs_solver
from solver.dfs_solver import dfs
from solver.ucs_solver import ucs
import time

def run_algorithm_comparison(map_id=1):
    """Compare all algorithms on a specific map"""
    print(f"🎯 Algorithm Comparison - Map {map_id}")
    print("=" * 50)
    
    # Load map
    vehicles = import_map(map_id)
    if not vehicles:
        print(f"❌ Failed to load map {map_id}")
        return
    
    initial_state = State(vehicles)
    print(f"Map loaded: {len(vehicles)} vehicles")
    print(f"Already solved: {initial_state.is_solved()}")
    print()
    
    algorithms = {
        'BFS': {'func': bfs_solver, 'name': 'Breadth-First Search'},
        'DFS': {'func': dfs, 'name': 'Depth-First Search'},
        'UCS': {'func': ucs, 'name': 'Uniform Cost Search'}
    }
    
    results = {}
    
    for algo_name, algo_info in algorithms.items():
        print(f"🚀 Running {algo_info['name']}...")
        
        try:
            start_time = time.time()
            result = algo_info['func'](initial_state)
            end_time = time.time()
            solve_time = end_time - start_time
            
            if result is not None:
                # Handle different return formats
                if algo_name == 'UCS':
                    cost, final_state, path = result
                    steps = len(path)
                    nodes_expanded = None
                elif algo_name == 'DFS':
                    # DFS returns just the path or None
                    if isinstance(result, list):
                        path = result
                        steps = len(path) if path else 0
                        cost = steps
                        nodes_expanded = None
                    else:
                        # No solution
                        results[algo_name] = {
                            'success': False,
                            'time': solve_time
                        }
                        print(f"   ❌ No solution found, Time={solve_time:.3f}s")
                        continue
                else:
                    # BFS, A* return (path, nodes_expanded, time)
                    if result[0] is not None:
                        path, nodes_expanded, _ = result
                        steps = len(path) if path else 0
                        cost = steps
                    else:
                        results[algo_name] = {
                            'success': False,
                            'time': solve_time
                        }
                        print(f"   ❌ No solution found, Time={solve_time:.3f}s")
                        continue
                
                results[algo_name] = {
                    'success': True,
                    'cost': cost,
                    'steps': steps,
                    'time': solve_time,
                    'nodes_expanded': nodes_expanded
                }
                
                nodes_str = f", Nodes: {nodes_expanded}" if nodes_expanded is not None else ""
                print(f"   ✅ Solution found: Cost={cost}, Steps={steps}, Time={solve_time:.3f}s{nodes_str}")
            else:
                results[algo_name] = {
                    'success': False,
                    'time': solve_time
                }
                print(f"   ❌ No solution found, Time={solve_time:.3f}s")
                
        except Exception as e:
            results[algo_name] = {
                'success': False,
                'error': str(e)
            }
            print(f"   💥 Error: {str(e)}")
    
    # Summary
    print(f"\n📊 COMPARISON SUMMARY")
    print("-" * 30)
    
    successful_algos = [name for name, result in results.items() if result.get('success', False)]
    
    if successful_algos:
        print(f"Successful algorithms: {', '.join(successful_algos)}")
        
        # Find best by different metrics
        best_time = min(successful_algos, key=lambda x: results[x]['time'])
        best_cost = min(successful_algos, key=lambda x: results[x]['cost'])
        
        print(f"⚡ Fastest: {best_time} ({results[best_time]['time']:.3f}s)")
        print(f"💰 Lowest cost: {best_cost} (cost={results[best_cost]['cost']})")
        
        # Show nodes expanded comparison if available
        algos_with_nodes = [name for name in successful_algos if results[name].get('nodes_expanded') is not None]
        if algos_with_nodes:
            best_nodes = min(algos_with_nodes, key=lambda x: results[x]['nodes_expanded'])
            print(f"🔍 Fewest nodes: {best_nodes} ({results[best_nodes]['nodes_expanded']} nodes)")
    else:
        print("❌ No algorithms found a solution.")

if __name__ == "__main__":
    print("🧪 Multi-Algorithm Rush Hour Demo")
    print("=" * 40)
    print()
    
    # Test on maps 1 and 2
    for map_id in [1, 2]:
        run_algorithm_comparison(map_id)
        print("\n" + "=" * 60 + "\n")
