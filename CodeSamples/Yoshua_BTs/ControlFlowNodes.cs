using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;

namespace TeamZlatan.BehaviorTrees
{
    class RootNode : TreeNode
    {
        private TreeNode child;

        public TreeNode Child { get { return child; } set { child = value; } }

        public void Init()
        {
            this.name = "root";
        }

        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.name = "root";
            this.data = data;
            this.child.Init(data);
        }

        override
        public NodeStatus Tick()
        {
            return child.Tick();
        }

        override
        public void Announce()
        {
            if(this.verbose)
                Console.WriteLine("Root node");
        }
    }


    class SelectorNode : TreeNode
    {
        protected TreeNode[] children;

        public TreeNode[] Children { get { return children; } set { children = value; } }

        public SelectorNode(String name)
        {
            this.name = name;
        }

        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
            foreach (TreeNode child in this.children)
            {
                child.Init(data);
            }
        }

        override
        public NodeStatus Tick()
        {
            Announce();
            foreach (TreeNode child in this.children)
            {
                NodeStatus childStatus = child.Tick();
                if (childStatus == NodeStatus.RUNNING)
                {
                    return NodeStatus.RUNNING;
                }
                if (childStatus == NodeStatus.SUCCESS)
                {
                    return NodeStatus.SUCCESS;
                }
            }
            return NodeStatus.FAILURE;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("    Selector " + this.name);
        }
    }


    class SequenceNode : TreeNode
    {
        protected TreeNode[] children;

        public TreeNode[] Children { get { return children; } set { children = value; } }

        public SequenceNode(String name)
        {
            this.name = name;
        }

        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
            foreach (TreeNode child in this.children)
            {
                child.Init(data);
            }
        }

        override
        public NodeStatus Tick()
        {
            Announce();
            foreach(TreeNode child in this.children)
            {
                NodeStatus childStatus = child.Tick();
                if (childStatus == NodeStatus.RUNNING)
                {
                    return NodeStatus.RUNNING;
                }
                if (childStatus == NodeStatus.FAILURE)
                {
                    return NodeStatus.FAILURE;
                }
            }
            return NodeStatus.SUCCESS;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("    Sequence " + this.name);
        }
    }


    class ParallelNode : TreeNode
    {
        protected TreeNode[] children;
        protected int K = 2;
        protected int L = 2;

        public TreeNode[] Children { get { return children; } set { children = value; } }

        public ParallelNode(String name)
        {
            this.name = name;
        }

        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
            foreach (TreeNode child in this.children)
            {
                child.Init(data);
            }
        }

        override
        public NodeStatus Tick()
        {
            Announce();
            int numSuccesses = 0;
            int numFailures = 0;

            foreach (TreeNode child in this.children)
            {
                NodeStatus childStatus = child.Tick();
                if (childStatus == NodeStatus.SUCCESS)
                {
                    numSuccesses++;
                }
                if (childStatus == NodeStatus.FAILURE)
                {
                    numFailures++;
                }
            }

            if(numSuccesses >= this.K)
            {
                return NodeStatus.SUCCESS;
            }
            if(numFailures >= this.L)
            {
                return NodeStatus.FAILURE;
            }

            return NodeStatus.RUNNING;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("    Parallel selector " + this.name);
        }
    }


    class DecoratorNode : TreeNode
    {
        public DecoratorNode(String name)
        {
            this.name = name;
        }

        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
        }

        override
        public NodeStatus Tick()
        {
            NodeStatus status = NodeStatus.SUCCESS;
            return status;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("    Decorator " + this.name);
        }
    }


    class PriorityNode : TreeNode
    {
        public PriorityNode(String name)
        {
            this.name = name;
        }

        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
        }

        override
        public NodeStatus Tick()
        {
            NodeStatus status = NodeStatus.SUCCESS;
            return status;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("    Priority selector " + this.name);
        }
    }
}
