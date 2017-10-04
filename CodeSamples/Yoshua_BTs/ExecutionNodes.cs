using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;

namespace TeamZlatan.BehaviorTrees
{
    abstract class ActionNode : TreeNode
    {
        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("        Action " + this.name);
        }
    }

    abstract class ConditionNode : TreeNode
    {
        override
        public void Init(Dictionary<string, dynamic> data)
        {
            this.data = data;
        }

        override
        public void Announce()
        {
            if (this.verbose)
                Console.WriteLine("        Condition " + this.name);
        }
    }
}
