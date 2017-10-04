using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;

namespace TeamZlatan.BehaviorTrees
{
    class BehaviorTree
    {
        private RootNode root;

        public BehaviorTree()
        {
            this.root = new RootNode();
        }

        public RootNode Root { get { return root; } set { root = value; } }

        public void Update(Dictionary<string, dynamic> data)
        {
            this.root.Init(data);
            this.root.Tick();
        }


    }
}
