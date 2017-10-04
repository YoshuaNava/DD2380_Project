using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections;

namespace TeamZlatan.BehaviorTrees
{
    abstract class TreeNode
    {
        /* Basic tree node parameters */
        protected String name;
        protected NodeStatus status;
        protected Dictionary<string, dynamic> data;

        /* Parameter to enable/disable command line output */
        protected bool verbose = true;

        #region GettersSetters
        public string Name { get { return name; } set { name = value; } }
        public NodeStatus Status { get { return status; } set { status = value; } }
        public Dictionary<string, dynamic> Data { get { return data; } set { data = value; } }
        #endregion



        public abstract void Init(Dictionary<string, dynamic> data);
        public abstract NodeStatus Tick();
        public abstract void Announce();
    }


    public enum NodeStatus
    {
        SUCCESS,
        FAILURE,
        RUNNING,
        ERROR
    }
}
